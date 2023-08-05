# Copyright (c) Microsoft Corporation. All rights reserved.
from .dataflow_generated import BaseDataflow, DataflowReference
from .engineapi.typedefinitions import (SkipMode, PromoteHeadersMode, FileEncoding,
                                        ExecuteAnonymousBlocksMessageArguments,
                                        ColumnsSelectorDetails, ColumnsSelectorType, SingleColumnSelectorDetails,
                                        ColumnsSelector, DataSourceTarget, CodeBlockType, FieldType, JoinType,
                                        ActivityReference, EndOfLineConvention, GetSecretsMessageArguments,
                                        AssertPolicy, AddBlockToListMessageArguments, BlockArguments)
from .dataprofile import DataProfile
from .datasources import MSSQLDataSource, LocalDataSource, DataSource, FileOutput
from .references import make_activity_reference
from .step import (Step, steps_to_block_datas, single_column_to_selector_value, MultiColumnSelection,
                   column_selection_to_selector_value)
from .typeconversions import (TypeConverter, DateTimeConverter)
from .types import SplitExample, Delimiters
from .expressions import Expression
from typing import List, Dict, cast, Tuple, TypeVar, Optional, Any
from pathlib import PurePath, Path
from textwrap import dedent, indent
from copy import copy
import random
import tempfile
import datetime
from uuid import uuid4


class Dataflow(BaseDataflow):
    """
    A Dataflow represents a series of lazily-evaluated, immutable operations on data.

    Dataflows are usually created by supplying a data source. Once the data source has been provided, operations can be
    added by invoking the different transformation methods available on this class. The result of adding an operation to
    a Dataflow is always a new Dataflow.

    The actual loading of the data and execution of the transformations is delayed as much as possible and will not
    occur until a 'pull' takes place. A pull is the action of reading data from a Dataflow, whether by asking to
    look at the first N records in it or by transferring the data in the Dataflow to another storage mechanism
    (a Pandas Dataframe, a CSV file, or a Spark Dataframe).

    The operations available on the Dataflow are runtime-agnostic. This allows the transformation pipelines contained
    in them to be portable between a regular Python environment and Spark.
    """
    _default_dataflow_name = 'dataflow'

    def _get_name_from_datasource(self):
        for step in self._steps:
            if step.step_type == 'Microsoft.DPrep.GetFilesBlock' or \
               step.step_type == 'Microsoft.DPrep.ReadExcelBlock' or \
               step.step_type == 'Microsoft.DPrep.ReadParquetDatasetBlock':
                if self._get_property_value(step.arguments['path'], 'target') is DataSourceTarget.LOCAL \
                        or self._get_property_value(step.arguments['path'], 'target') == DataSourceTarget.LOCAL.value:
                    # noinspection PyBroadException
                    try:
                        path = PurePath(step.arguments['path'].resource_details[0].to_pod()['path'])
                        return path.stem
                    except Exception:
                        return None
        return None

    @staticmethod
    def _get_property_value(property, property_name: str):
        return property[property_name] if isinstance(property, dict) else property.to_pod()[property_name]

    @property
    def name(self):
        if self._name is None:
            self._name = self._get_name_from_datasource() or Dataflow._default_dataflow_name
        return self._name

    def set_name(self, name: str):
        cloned_df = copy(self)
        cloned_df._name = name
        cloned_df.id = uuid4()
        return cloned_df

    def get_steps(self) -> List[Step]:
        return [s for s in self._steps]

    def get_profile(self) -> DataProfile:
        """
        Request the data profile which collects summary statistics on the data produced by Dataflow.

        :return: The data profile.
        """
        self._raise_if_missing_secrets()
        return DataProfile(self._engine_api, make_activity_reference(self))

    # noinspection PyUnresolvedReferences
    def head(self, count: int) -> 'pandas.DataFrame':
        """
        Pulls the number of records specified from this Dataflow and returns them as a Pandas Dataframe.

        :param count: The number of records to pull.
        :return: A Pandas Dataframe.
        """
        return self.take(count).to_pandas_dataframe(extended_types=True)

    def run_local(self) -> None:
        """
        Runs the current Dataflow using the local execution runtime.
        """
        self._raise_if_missing_secrets()
        self._engine_api.execute_anonymous_blocks(ExecuteAnonymousBlocksMessageArguments(
            blocks=steps_to_block_datas(self._steps),
            project_context=self._parent_package_path
        ))

    def run_spark(self) -> None:
        """
        Runs the current Dataflow using the Spark runtime.
        """
        self._raise_if_missing_secrets()
        return self._spark_executor.execute(steps_to_block_datas(self._steps),
                                            project_context=self._parent_package_path,
                                            use_sampling=False)

    # noinspection PyUnresolvedReferences
    def to_pandas_dataframe(self, extended_types: bool = False) -> 'pandas.DataFrame':
        from azureml.dataprep.native import preppy_to_ndarrays
        """
        Pulls all of the data and returns it in the form of a Pandas Dataframe, which is fully materialized in memory.

        Since Dataflows do not require a fixed, tabular schema but Pandas Dataframes do, an implicit tabularization
        step will be executed as part of this action. The resulting schema will be the union of the schemas of all
        records produced by this Dataflow.

        :param extended_types: Whether to keep extended DataPrep types such as DataPrepError in the DataFrame. If False,
            these values will be replaced with None.
        :return: A Pandas Dataframe.
        """
        from collections import OrderedDict
        try:
            import pandas
        except ImportError:
            raise RuntimeError('Pandas is not installed. To use pandas with azureml.dataprep, '
                               'pip install azureml-dataprep[pandas].')

        intermediate_path = Path(tempfile.mkdtemp())
        dataflow_to_execute = self.add_step('Microsoft.DPrep.WriteDataSetBlock', {
            'outputPath': {
                'target': 0,
                'resourceDetails': [{'path': str(intermediate_path)}]
            },
            'profilingFields': ['Schema', 'DataQuality']
        })

        self._raise_if_missing_secrets()
        self._engine_api.execute_anonymous_blocks(
            ExecuteAnonymousBlocksMessageArguments(blocks=steps_to_block_datas(dataflow_to_execute._steps),
                                                   project_context=self._parent_package_path))

        intermediate_files = [str(p) for p in intermediate_path.glob('part-*')]
        intermediate_files.sort()
        dataset = preppy_to_ndarrays(intermediate_files, extended_types)
        return pandas.DataFrame.from_dict(OrderedDict(dataset))

    # noinspection PyUnresolvedReferences
    def to_spark_dataframe(self) -> 'pyspark.sql.DataFrame':
        """
        Creates a Spark Dataframe that can execute the transformation pipeline defined by this Dataflow.

        Since Dataflows do not require a fixed, tabular schema but Spark Dataframes do, an implicit tabularization
        step will be executed as part of this action. The resulting schema will be the union of the schemas of all
        records produced by this Dataflow. This tabularization step will result in a pull of the data.

        The Spark Dataframe returned is only an execution plan and doesn't actually contain any data, since Spark
        Dataframes are also lazily evaluated.

        :return: A Spark Dataframe.
        """
        self._raise_if_missing_secrets()
        return self._spark_executor.get_dataframe(steps_to_block_datas(self._steps),
                                                  project_context=self._parent_package_path,
                                                  use_sampling=False)

    def parse_delimited(self,
                        separator: str,
                        headers_mode: PromoteHeadersMode,
                        encoding: FileEncoding,
                        quoting: bool,
                        skip_rows: int,
                        skip_mode: SkipMode,
                        comment: str) -> 'Dataflow':
        return self.add_step('Microsoft.DPrep.ParseDelimitedBlock', {
            'columnHeadersMode': headers_mode,
            'separator': separator,
            'commentLineCharacter': comment,
            'fileEncoding': encoding,
            'skipRowsMode': skip_mode,
            'skipRows': skip_rows,
            'handleQuotedLineBreaks': quoting
        })

    def parse_fwf(self,
                  offsets: List[int],
                  headers_mode: PromoteHeadersMode,
                  encoding: FileEncoding,
                  skip_rows: int,
                  skip_mode: SkipMode) -> 'Dataflow':
        return self.add_step('Microsoft.DPrep.ParseFixedWidthColumns', {
            'columnHeadersMode': headers_mode,
            'columnOffsets': offsets,
            'fileEncoding': encoding,
            'skipRowsMode': skip_mode,
            'skipRows': skip_rows,
        })

    def parse_lines(self,
                    headers_mode: PromoteHeadersMode,
                    encoding: FileEncoding,
                    skip_rows: int,
                    skip_mode: SkipMode,
                    comment: str) -> 'Dataflow':
        return self.add_step('Microsoft.DPrep.ParsePlainTextBlock', {
            'columnHeadersMode': headers_mode,
            'commentLineCharacter': comment,
            'fileEncoding': encoding,
            'skipRowsMode': skip_mode,
            'skipRows': skip_rows
        })

    def read_sql(self, data_source: MSSQLDataSource, query: str):
        return self.add_step('Database', {
            'server': data_source.server,
            'database': data_source.database,
            'credentialsType': data_source.credentials_type,
            'credentials': {
                'userName': data_source.userName,
                'password': data_source.password
            },
            'query': query,
            'trustServer': data_source.trustServer
        })

    def read_parquet_file(self) -> 'Dataflow':
        return self.add_step('Microsoft.DPrep.ReadParquetFileBlock', {})

    def read_json(self,
                  json_extract_program: str,
                  encoding: FileEncoding):
        return self.add_step('JSONFile', {
            'dsl': json_extract_program,
            'fileEncoding': encoding
        })

    def set_column_types(self, type_conversions: Dict[str, TypeConverter]) -> 'Dataflow':

        def _get_type_arguments(converter: TypeConverter):
            if not isinstance(converter, DateTimeConverter):
                return None

            return {'dateTimeFormats': converter.formats}

        def _are_all_date_formats_available(conversions: List[Any]) -> bool:
            for conversion in conversions:
                if conversion['typeProperty'] == FieldType.DATE:
                    if conversion.get('typeArguments') is None \
                            or conversion['typeArguments']['dateTimeFormats'] is None \
                            or len(conversion['typeArguments']['dateTimeFormats']) == 0:
                        return False

            return True

        arguments = {'columnConversion': [{
            'column': ColumnsSelector(type=ColumnsSelectorType.SINGLECOLUMN,
                                      details=cast(ColumnsSelectorDetails, SingleColumnSelectorDetails(col))),
            'typeProperty': converter.data_type,
            'typeArguments': _get_type_arguments(converter)
        } for col, converter in type_conversions.items()]}

        need_to_learn = not _are_all_date_formats_available(arguments['columnConversion'])

        if need_to_learn:
            blocks = steps_to_block_datas(self.get_steps())
            set_column_types_block = self._engine_api.add_block_to_list(
                AddBlockToListMessageArguments(blocks=blocks,
                                               new_block_arguments=BlockArguments(arguments, 'Microsoft.DPrep.SetColumnTypesBlock'),
                                               project_context=self.parent_package_path))
            learned_arguments = set_column_types_block.arguments.to_pod()
            success = _are_all_date_formats_available(learned_arguments['columnConversion'])
            if not success:
                raise ValueError('Can\'t detect date_time_formats automatically, please provide desired formats.')

            arguments = learned_arguments

        return self.add_step('Microsoft.DPrep.SetColumnTypesBlock', arguments)

    def take_sample(self,
                    probability: float,
                    seed: Optional[int] = None) -> 'Dataflow':
        """
        Takes a random sample of the available records.

        :param probability: The probability of a record being included in the sample.
        :param seed: The seed to use for the random generator.
        :return: The modified Dataflow.
        """
        return self.add_step('Microsoft.DPrep.TakeSampleBlock', {
            'probability': probability,
            'seed': seed or random.randint(0, 4294967295)
        })

    def filter(self, expression: Expression) -> 'Dataflow':
        """
        Filters the data, leaving only the records that match the specified expression.

        Expressions are built using expression builders (col, f_and, f_or, f_not, etc). The resulting expression
        will be lazily evaluated for each record when a data pull occurs and not where it is defined.

        Example:
        col('myColumn') > col('columnToCompareAgainst')
        col('myColumn').starts_with('prefix')

        :param expression: The expression to evaluate.
        :return: The modified Dataflow.
        """
        return self.add_step('Microsoft.DPrep.ExpressionFilterBlock', {'expression': expression.underlying_data})

    def add_column(self, expression: Expression, new_column_name: str, prior_column: str) -> 'Dataflow':
        """
        Adds a new column to the dataset. The value for each row will be the result of invoking the specified
        expression.

        Expressions are built using the expression builders in the expressions module and the functions in
        the functions module. The resulting expression will be lazily evaluated for each record when a data pull
        occurs and not where it is defined.

        :param expression: The expression to evaluate to generate the values in the column.
        :param new_column_name: The name of the new column.
        :param prior_column: The column after which the new column should be added.
        :return: The modified Dataflow.
        """
        return self.add_step('Microsoft.DPrep.ExpressionAddColumnBlock', {
            'expression': expression.underlying_data,
            'newColumnName': new_column_name,
            'priorColumn': single_column_to_selector_value(prior_column) if prior_column is not None else None
        })

    ExampleData = TypeVar('ExampleData', Tuple[str, str], Tuple[Dict[str, str], str], List[Tuple[str, str]],
                          List[Tuple[Dict[str, str], str]])
    SourceColumns = TypeVar('SourceColumns', str, List[str])

    def derive_column_by_example(self,
                                 source_columns: SourceColumns,
                                 new_column_name: str,
                                 example_data: ExampleData) -> 'Dataflow':
        """
        Inserts a column by learning a program based on a set of source columns and provided examples.
        If you need more control of examples and generated program, create DeriveColumnByExampleBuilder instead.

        :param source_columns: Names of columns that should be considered as source.
        :param new_column_name: Name of the new column to add.
        :param example_data: Examples to use as input for program generation.
            In case there is only one column to be used as source, examples could be Tuples of source value and intended
            target value.
            When multiple columns should be considered as source, each example should be a Tuple of dict-like sources
            and intended target value, where sources have column names as keys and column values as values.
        :return: The modified Dataflow.
        """

        if isinstance(source_columns, str):
            # for single source column case create a list for uniform processing
            source_columns = [source_columns]
        else:
            try:
                source_columns = [s for s in source_columns]
            except TypeError:
                source_columns = []

        if len(source_columns) == 0:
            raise ValueError('Please provide columns to derive from')

        if not isinstance(example_data, List):
            # for single example case create a list for uniform processing
            example_data = [example_data]

        source_data_and_examples = []
        for example_data_entry in example_data:
            if not isinstance(example_data_entry[1], str):
                raise ValueError('Incorrect example data. "example_data" should be either '
                                 'Tuple[str|Dict[str, str], str], or List[Tuple[str|Dict[str, str], str]]')
            if isinstance(example_data_entry[0], Dict):
                source_data_and_examples.append(example_data_entry)
            elif len(source_columns) == 1:
                source_data_and_examples.append((
                    {source_columns[0]: str(example_data_entry[0])},
                    example_data_entry[1]))
            else:
                raise ValueError('Incorrect example data. When you derive from multiple columns "example_data" should '
                                 'be either Tuple[Dict[str, str], str] or List[Tuple[Dict[str, str], str]]')

        derive_column_builder = self.builders.derive_column_by_example(source_columns, new_column_name)

        for item in source_data_and_examples:
            derive_column_builder.add_example(source_data=item[0], example_value=item[1])

        return derive_column_builder.to_dataflow()

    def fuzzy_group_column(self,
                           source_column: str,
                           new_column_name: str,
                           similarity_threshold: float = 0.8,
                           similarity_score_column_name: str = None) -> 'Dataflow':
        """
        Add a column where similar values from the source column are fuzzy-grouped to their canonical form.
        If you need more control of grouping, create FuzzyGroupBuilder instead.

        :param source_column: Column with values to group.
        :param new_column_name: Name of the new column to add.
        :param similarity_threshold: Similarity between values to be grouped together.
        :param similarity_score_column_name: If provided, this transform will also add a column with calculated
            similarity score.
        :return: The modified Dataflow.
        """
        builder = self.builders.fuzzy_group_column(source_column,
                                                   new_column_name,
                                                   similarity_threshold,
                                                   similarity_score_column_name)
        return builder.to_dataflow()

    def one_hot_encode(self, source_column: str, prefix: str = None) -> 'Dataflow':
        """
        Adds a binary column for each categorical label from the source column values. For more control over categorical labels, use OneHotEncodingBuilder.

        :param source_column: Column name from which categorical labels will be generated.
        :return: The modified Dataflow.
        """
        builder = self.builders.one_hot_encode(source_column, prefix)
        return builder.to_dataflow()

    def label_encode(self, source_column: str, new_column_name: str) -> 'Dataflow':
        """
        Adds a column with encoded labels generated from the source column. For explicit label encoding, use LabelEncoderBuilder.

        :param source_column: Column name from which encoded labels will be generated.
        :param new_column_name: The new column's name.
        :return: The modified Dataflow.
        """
        builder = self.builders.label_encode(source_column, new_column_name)
        return builder.to_dataflow()

    def quantile_transform(self, source_column: str, new_column: str,
                           quantiles_count: int = 1000, output_distribution: str = 'Uniform'):
        """
        Perform quantile transformation to the source_column and output the transformed result in new_column.

        :param source_column: The column which quantile transform will be applied to.
        :param new_column: The column where the transformed data will be placed.
        :param quantiles_count: The number of quantiles used. This will be used to discretize the cdf, defaults to 1000
        :param output_distribution: The distribution of the transformed data, defaults to 'Uniform'
        :return: The modified Dataflow.
        """
        return self.builders \
            .quantile_transform(source_column, new_column, quantiles_count, output_distribution) \
            .to_dataflow()

    def min_max_scale(self,
                      column: str,
                      range_min: float = 0,
                      range_max: float = 1,
                      data_min: float = None,
                      data_max: float = None) -> 'Dataflow':
        """
        Scales the values in the specified column to lie within range_min (default=0) and range_max (default=1).

        :param column: The column to scale.
        :param range_min: Desired min of scaled values.
        :param range_max: Desired max of scaled values.
        :param data_min: Min of source column. If not provided, a scan of the data will be performed to find the min.
        :param data_max: Max of source column. If not provided, a scan of the data will be performed to find the max.
        :return: The modified Dataflow.
        """
        builder = self.builders.min_max_scale(column, range_min, range_max, data_min, data_max)
        return builder.to_dataflow()

    def replace_datasource(self, new_datasource: DataSource) -> 'Dataflow':
        """
        Returns new Dataflow with its DataSource replaced by the given one.

        The given 'new_datasource' must match the type of datasource already in the Dataflow.
        For example a MSSQLDataSource cannot be replaced with a FileDataSource.

        :param new_datasource: DataSource to substitute into new Dataflow.
        :return: The modified Dataflow.
        """
        if isinstance(new_datasource, MSSQLDataSource):
            if not self._steps[0].step_type == 'Database':
                raise ValueError("Can't replace '" + self._steps[0].step_type + "' Datasource with MSSQLDataSource.")
            from .readers import read_sql
            new_datasource_step = read_sql(new_datasource, self._steps[0].arguments['query']).get_steps()[0]
            new_datasource_step.id = self._steps[0].id
        else:
            if self._steps[0].step_type == 'Database':
                raise ValueError("Can only replace 'Database' Datasource with MSSQLDataSource.")
            import copy
            new_datasource_step = copy.deepcopy(self._steps[0])
            new_datasource_step.arguments['path'] = new_datasource.underlying_value
        return Dataflow(self._engine_api,
                        [new_datasource_step] + self._steps[1:],
                        self._name,
                        self.id,
                        self._parent_package_path)

    def replace_reference(self, new_reference: DataflowReference) -> 'Dataflow':
        """
        Returns new Dataflow with its reference DataSource replaced by the given one.

        :param new_reference: Reference to be substituted for current Reference in Dataflow.
        :return: The modified Dataflow.
        """
        if self._steps[0].step_type != 'Microsoft.DPrep.ReferenceBlock':
            raise ValueError("Can only replace 'Reference' Datasource with 'DataflowReference', found: " +
                             self._steps[0].step_type)
        new_reference_step = Dataflow.reference(new_reference).get_steps()[0]
        new_reference_step.id = self._steps[0].id
        return Dataflow(self._engine_api,
                        [new_reference_step] + self._steps[1:],
                        self._name,
                        self.id,
                        self._parent_package_path)

    def cache(self, directory_path: str) -> 'Dataflow':
        """
        Pulls all the records from this Dataflow and cache the result to disk.

        This is very useful when data is accessed repeatedly, as future executions will reuse
        the cached result without pulling the same Dataflow again.

        :param directory_path: The directory to save cache files.
        :return: The modified Dataflow.
        """
        df = self.add_step('Microsoft.DPrep.CacheBlock', {
            'cachePath': LocalDataSource(directory_path).underlying_value
        })
        df.head(1)
        return df

    def new_script_column(self,
                          new_column_name: str,
                          insert_after: str,
                          script: str) -> 'Dataflow':
        """
        Adds a new column to the Dataflow using the passed in Python script.

        The Python script must define a function called newvalue that takes a single argument, typically
        called row. The row argument is a dict (key is column name, value is current value) and will be passed
        to this function for each row in the dataset. This function must return a value to be used in the new column.
        Any libraries that the Python script imports must exist in the environment where the dataflow is run.

        Example:

        .. code:: python

            import numpy as np
            def newvalue(row):
                return np.log(row['Metric'])

        :param new_column_name: The name of the new column being created.
        :param insert_after: The column after which the new column will be inserted.
        :param script: The script that will be used to create this new column.
        :return: The modified Dataflow.
        """
        return self.add_step(step_type='Microsoft.DPrep.AddCustomColumnBlock', arguments={
            "codeBlockType": CodeBlockType.MODULE,
            "columnId": new_column_name,
            "customExpression": script,
            "priorColumnId": ColumnsSelector(
                                type=ColumnsSelectorType.SINGLECOLUMN,
                                details=cast(ColumnsSelectorDetails, SingleColumnSelectorDetails(insert_after)))
          })

    def new_script_filter(self,
                          script: str) -> 'Dataflow':
        """
        Filters the Dataflow using the passed in Python script.

        The Python script must define a function called includerow that takes a single argument, typically
        called row. The row argument is a dict (key is column name, value is current value) and will be passed
        to this function for each row in the dataset. This function must return True or False depending on whether
        the row should be included in the dataflow. Any libraries that the Python script imports must exist in the
        environment where the dataflow is run.

        Example:

        .. code:: python

            def includerow(row):
                return row['Metric'] > 100

        :param script: The script that will be used to filter the dataflow.
        :return: The modified Dataflow.
        """
        return self.add_step(step_type='Microsoft.DPrep.FilterBlock', arguments={
            "codeBlockType": CodeBlockType.MODULE,
            "filterExpression": script
          })

    def transform_partition(self,
                            script: str) -> 'Dataflow':
        """
        Transforms an entire partition using the passed in Python script.

        The Python script must define a function called transform that takes two arguments, typically called df and
        index. The df argument will be a pandas dataframe passed to this function that contains the data for the
        partition and the index argument is a unique identifier of the partition. Note that df does not usually contain
        all of the data in the dataflow, but a partition of the data as it is being processed in the runtime.
        The number and contents of each partition is not guaranteed across runs.

        The transform function can fully edit the passed in dataframe or even create a new one, but must return a
        dataframe. Any libraries that the Python script imports must exist in the environment where the dataflow is run.

        Example:

        .. code:: python

            def transform(df, index):
                return df

        :param script: The script that will be used to transform the partition.
        :return: The modified Dataflow.
        """
        return self.add_step(step_type='Microsoft.DPrep.MapPartitionsAsDataFrameBlock', arguments={
            "codeBlockType": CodeBlockType.MODULE,
            "MapPartitionsAsDataFrameBlock": script
          })

    def transform_partition_with_file(self,
                                      script_path: str) -> 'Dataflow':
        """
        Transforms an entire partition using the Python script in the passed in file.

        The Python script must define a function called transform that takes two arguments, typically called df and
        index. The first argument (df) will be a pandas dataframe that contains the data for the partition and the
        second argument (index) will be a unique identifier for the partition. Note that df does not usually contain
        all of the data in the dataflow, but a partition of the data as it is being processed in the runtime.
        The number and contents of each partition is not guaranteed across runs.

        The transform function can fully edit the passed in dataframe or even create a new one, but must return a
        dataframe. Any libraries that the Python script imports must exist in the environment where the dataflow is run.

        Example:

        .. code:: python

            def transform(df, index):
                return df

        :param script_path: Relative path to script that will be used to transform the partition.
        :return: The modified Dataflow.
        """
        return self.add_step(step_type='Microsoft.DPrep.MapPartitionsAsDataFrameBlock', arguments={
            "codeBlockType": CodeBlockType.FILE,
            "MapPartitionsAsDataFrameBlock": script_path
        })

    def split_column_by_delimiters(self,
                                   source_column: str,
                                   delimiters: Delimiters,
                                   keep_delimiters: False) -> 'Dataflow':
        """
        Splits the provided column and adds the resulting columns to the dataflow.

        This will pull small sample of the data, determine number of columns it should expect as a result of the split
        and generate a split program that would ensure that the expected number of columns will be produced, so that
        there is a deterministic schema after this operation.

        :param source_column: Column to split.
        :param delimiters: String or list of strings to be deemed as column delimiters.
        :param keep_delimiters: Controls whether to keep or drop column with delimiters.
        :return: The modified Dataflow.
        """
        builder = self.builders.split_column_by_example(source_column=source_column,
                                                        delimiters=delimiters,
                                                        keep_delimiters=keep_delimiters)
        return builder.to_dataflow()

    def split_column_by_example(self, source_column: str, example: SplitExample = None) -> 'Dataflow':
        """
        Splits the provided column and adds the resulting columns to the dataflow based on the provided example.

        This will pull small sample of the data, determine the best program to satisfy provided example
        and generate a split program that would ensure that the expected number of columns will be produced, so that
        there is a deterministic schema after this operation.

        If example is not provided, this will generate a split program based on common split patterns.

        :param source_column: Column to split.
        :param example: Example to use for program generation.
        :return: The modified Dataflow.
        """
        builder = self.builders.split_column_by_example(source_column=source_column)
        if example is not None:
            builder.add_example(example)
        return builder.to_dataflow()

    def replace(self,
                columns: MultiColumnSelection,
                find: Any,
                replace_with: Any) -> 'Dataflow':
        """
        Replaces values in a column that match the specified search value.

        The following types are supported for both the find or replace arguments: str, int, float,
        datetime.datetime, and bool.

        :param columns: The source columns.
        :param find: The value to find, or None.
        :param replace_with: The replacement value, or None.
        :return: The modified Dataflow.
        """
        replace_dict = self._make_replace_dict(find, replace_with)

        if replace_dict['valueToFindType'] == FieldType.UNKNOWN:
            raise ValueError('The type of the find argument is not supported')
        if replace_dict['replaceWithType'] == FieldType.UNKNOWN:
            raise ValueError('The type of the replace_with argument is not supported')

        return self._add_replace_step(columns, replace_dict)

    def error(self,
              columns: MultiColumnSelection,
              find: Any,
              error_code: str) -> 'Dataflow':
        """
        Creates errors in a column for values that match the specified search value.

        The following types are supported for the find argument: str, int, float,
        datetime.datetime, and bool.

        :param columns: The source columns.
        :param find: The value to find, or None.
        :param error_code: The error code to use in new errors, or None.
        :return: The modified Dataflow.
        """
        replace_dict = self._make_replace_dict(find, None)

        if replace_dict['valueToFindType'] == FieldType.UNKNOWN:
            raise ValueError('The type of the find argument is not supported')
        replace_dict['replaceWithType'] = FieldType.ERROR

        return self._add_replace_step(columns, replace_dict, error_code)

    def fill_nulls(self,
                   columns: MultiColumnSelection,
                   fill_with: Any) -> 'Dataflow':
        """
        Fills all nulls in a column with the specified value.

        The following types are supported for the fill_with argument: str, int, float,
        datetime.datetime, and bool.

        :param columns: The source columns.
        :param fill_with: The value to fill nulls with.
        :return: The modified Dataflow.
        """
        replace_dict = self._make_replace_dict(None, fill_with)

        replace_dict['valueToFindType'] = FieldType.NULL
        if replace_dict['replaceWithType'] == FieldType.UNKNOWN or replace_dict['replaceWithType'] == FieldType.NULL:
            raise ValueError('The type of the fill_with argument is not supported')

        return self._add_replace_step(columns, replace_dict)

    def fill_errors(self,
                    columns: MultiColumnSelection,
                    fill_with: Any) -> 'Dataflow':
        """
        Fills all errors in a column with the specified value.

        The following types are supported for the fill_with argument: str, int, float,
        datetime.datetime, and bool.

        :param columns: The source columns.
        :param fill_with: The value to fill errors with, or None.
        :return: The modified Dataflow.
        """
        replace_dict = self._make_replace_dict(None, fill_with)

        replace_dict['valueToFindType'] = FieldType.ERROR
        if replace_dict['replaceWithType'] == FieldType.UNKNOWN:
            raise ValueError('The type of the fill_with argument is not supported')

        return self._add_replace_step(columns, replace_dict)

    def join(self,
             right_dataflow: DataflowReference,
             join_key_pairs: List[Tuple[str, str]] = None,
             join_type: JoinType = JoinType.MATCH,
             left_column_prefix: str = 'l_',
             right_column_prefix: str = 'r_',
             left_non_prefixed_columns: List[str] = None,
             right_non_prefixed_columns: List[str] = None) -> 'Dataflow':
        """
        Creates a new Dataflow that is a result of joining this Dataflow with the provided right_dataflow.

        :param right_dataflow: Right Dataflow or DataflowReference to join with.
        :param join_key_pairs: Key column pairs. List of tuples of columns names where each tuple forms a key pair to
            join on. For instance: [('column_from_left_dataflow', 'column_from_right_dataflow')]
        :param join_type: Type of join to perform. Match is default.
        :param left_column_prefix: Prefix to use in result Dataflow for columns originating from left_dataflow.
            Needed to avoid column name conflicts at runtime.
        :param right_column_prefix: Prefix to use in result Dataflow for columns originating from right_dataflow.
            Needed to avoid column name conflicts at runtime.
        :param left_non_prefixed_columns: List of column names from left_dataflow that should not be prefixed with
            left_column_prefix. Every other column appearing in the data at runtime will be prefixed.
        :param right_non_prefixed_columns: List of column names from right_dataflow that should not be prefixed with
            left_column_prefix. Every other column appearing in the data at runtime will be prefixed.
        :return: The new Dataflow.
        """

        return Dataflow.join(self,
                             right_dataflow,
                             join_key_pairs,
                             join_type,
                             left_column_prefix,
                             right_column_prefix,
                             left_non_prefixed_columns,
                             right_non_prefixed_columns)

    def write_to_csv(self,
                     directory_path: FileOutput,
                     eol: EndOfLineConvention = EndOfLineConvention.UNIX,
                     separator: str = ',',
                     na: str = 'NA',
                     error: str = 'ERROR') -> 'Dataflow':
        """
        Write out the data in the Dataflow in a delimited text format. The output is specified as a directory which will
        contain multiple files, one per partition processed in the Dataflow.

        :param directory_path: The path to a directory in which to store the output files.
        :param eol: The end-of-line character convention (Unix or Windows)
        :param separator: The separator to use.
        :param na: String to use for null values.
        :param error: String to use for error values.
        :return: The modified Dataflow. Every execution of the returned Dataflow will perform the write again.
        """
        return self.add_step('Microsoft.DPrep.WriteToCsvBlock', {
            'filePath': None,
            'directoryPath': directory_path.underlying_value,
            'eol': eol.value,
            'separator': separator,
            'singleFile': False,
            'na': na,
            'error': error
        })

    SortColumns = TypeVar('SortColumns', str, List[str])

    def sort_asc(self, columns: SortColumns) -> 'Dataflow':
        """
        Sorts the dataset in ascending order by the specified columns.

        :param columns: The columns to sort in ascending order.
        :return: The modified Dataflow.
        """
        columns = [columns] if not isinstance(columns, List) else columns
        return self.add_step('Microsoft.DPrep.SortBlock', {
             'sortOrder': [{'column': single_column_to_selector_value(c), 'descending': False} for c in columns]
         })

    def sort_desc(self, columns: SortColumns) -> 'Dataflow':
        """
        Sorts the dataset in descending order by the specified columns.

        :param columns: The columns to sort in descending order.
        :return: The modified Dataflow.
        """
        columns = [columns] if not isinstance(columns, List) else columns
        return self.add_step('Microsoft.DPrep.SortBlock', {
            'sortOrder': [{'column': single_column_to_selector_value(c), 'descending': True} for c in columns]
        })

    def to_datetime(self,
                    columns: MultiColumnSelection,
                    date_time_formats: Optional[List[str]] = None,
                    date_constant: Optional[str] = None) -> 'dataprep.api.dataflow.Dataflow':
        """
        Converts the values in the specified columns to DateTimes.

        :param columns: The source columns.
        :param date_time_formats: The formats to use to parse the values. If none are provided, a partial scan of the data will be performed to derive one.
        :param date_constant: If the column contains only time values, a date to apply to the resulting DateTime.
        :return: The modified Dataflow.
        """
        arguments = {
            'columns': column_selection_to_selector_value(columns),
            'dateTimeFormats': [p for p in date_time_formats] if date_time_formats is not None else None,
            'dateConstant': date_constant
        }

        if date_time_formats is None or len(date_time_formats) == 0:
            blocks = steps_to_block_datas(self.get_steps())
            to_datetime_block = self._engine_api.add_block_to_list(
                AddBlockToListMessageArguments(blocks=blocks,
                                               new_block_arguments=BlockArguments(arguments, 'Microsoft.DPrep.ToDateTimeBlock'),
                                               project_context=self.parent_package_path))
            learned_arguments = to_datetime_block.arguments.to_pod()
            if learned_arguments.get('dateTimeFormats') is None or len(learned_arguments['dateTimeFormats']) == 0:
                raise ValueError('Can\'t detect date_time_formats automatically, please provide desired formats.')

            arguments['dateTimeFormats'] = learned_arguments['dateTimeFormats']

        return self.add_step('Microsoft.DPrep.ToDateTimeBlock', arguments)

    def assert_value(self,
                     columns: MultiColumnSelection,
                     expression: Expression,
                     policy: AssertPolicy = AssertPolicy.ERRORVALUE,
                     error_code: str = 'AssertionFailed') -> 'Dataflow':
        """
        Ensures that values in the specified columns satisfy the provided expression.

        :param columns: Columns to apply evaluation to.
        :param expression: Expression that has to be evaluated to True for the value to be kept.
        :param policy: Action to take when expression is evaluated to False. Could be either FAILEXECUTION or ERRORVALUE
        :param error_code: Error to use to replace values failing the assertion or fail an execution.
        :return: The modified Dataflow.
        """
        return self.add_step('Microsoft.DPrep.ExpressionAssertValueBlock', {
            'columns': column_selection_to_selector_value(columns),
            'expression': expression.underlying_data,
            'assertPolicy': policy,
            'errorCode': error_code
        })

    def get_missing_secrets(self) -> List[str]:
        """
        Get a list of missing secret IDs.

        :return: A list of missing secret IDs.
        """
        secrets = self._engine_api.get_secrets(GetSecretsMessageArguments(
            steps_to_block_datas(self._steps),
            self._parent_package_path
        ))
        missing_secret_ids = map(
            lambda secret: secret.key,
            filter(lambda secret: not secret.is_available, secrets)
        )

        return list(missing_secret_ids)

    def use_secrets(self, secrets: Dict[str, str]):
        """
        Uses the passed in secrets for execution.

        :param secrets: A dictionary of secret ID to secret value. You can get the list of required secrets by calling
            the get_missing_secrets method on Dataflow.
        """
        self._engine_api.add_temporary_secrets(secrets)

    @classmethod
    def open(cls, file_path: str, name: str) -> 'Dataflow':
        """
        Opens a Dataflow with specified name from the package file.

        :param file_path: Path to the package containing the Dataflow.
        :param name: Name of the Dataflow to load.

        :return: The Dataflow.
        """
        from .package import Package
        pkg = Package.open(file_path)
        try:
            return next(df for df in pkg.dataflows if df.name == name)
        except StopIteration:
            raise NameError('Dataflow with name: ' + name + ', not found in supplied package.')

    @staticmethod
    def _datetime_for_message(dt: datetime):
        t = {'timestamp': int(dt.timestamp() * 1000)}
        return t

    def _make_replace_dict(self, find: Any, replace_with: Any):
        replace_dict = {
            'valueToFindType': FieldType.UNKNOWN,
            'stringValueToFind': None,
            'doubleValueToFind': None,
            'datetimeValueToFind': None,
            'booleanValueToFind': None,
            'replaceWithType': FieldType.UNKNOWN,
            'stringReplaceWith': None,
            'doubleReplaceWith': None,
            'datetimeReplaceWith': None,
            'booleanReplaceWith': None
        }

        if find is None:
            replace_dict['valueToFindType'] = FieldType.NULL
        elif isinstance(find, str):
            replace_dict['valueToFindType'] = FieldType.STRING
            replace_dict['stringValueToFind'] = find
        elif isinstance(find, int) or isinstance(find, float):
            replace_dict['valueToFindType'] = FieldType.DECIMAL
            replace_dict['doubleValueToFind'] = find
        elif isinstance(find, datetime.datetime):
            replace_dict['valueToFindType'] = FieldType.DATE
            replace_dict['datetimeValueToFind'] = self._datetime_for_message(find)
        elif isinstance(find, bool):
            replace_dict['valueToFindType'] = FieldType.BOOLEAN
            replace_dict['booleanValueToFind'] = find

        if replace_with is None:
            replace_dict['replaceWithType'] = FieldType.NULL
        elif isinstance(replace_with, str):
            replace_dict['replaceWithType'] = FieldType.STRING
            replace_dict['stringReplaceWith'] = replace_with
        elif isinstance(replace_with, int) or isinstance(replace_with, float):
            replace_dict['replaceWithType'] = FieldType.DECIMAL
            replace_dict['doubleReplaceWith'] = replace_with
        elif isinstance(replace_with, datetime.datetime):
            replace_dict['replaceWithType'] = FieldType.DATE
            replace_dict['datetimeReplaceWith'] = self._datetime_for_message(replace_with)
        elif isinstance(replace_with, bool):
            replace_dict['replaceWithType'] = FieldType.BOOLEAN
            replace_dict['booleanReplaceWith'] = replace_with

        return replace_dict

    def _add_replace_step(self, columns: MultiColumnSelection, replace_dict: Dict, error_replace_with: str = None):
        error_replace_with = str(error_replace_with) if error_replace_with is not None else None
        return self.add_step('Microsoft.DPrep.ReplaceBlock', {
                                 'columns': column_selection_to_selector_value(columns),
                                 'valueToFindType': replace_dict['valueToFindType'],
                                 'stringValueToFind': replace_dict['stringValueToFind'],
                                 'doubleValueToFind': replace_dict['doubleValueToFind'],
                                 'datetimeValueToFind': replace_dict['datetimeValueToFind'],
                                 'booleanValueToFind': replace_dict['booleanValueToFind'],
                                 'replaceWithType': replace_dict['replaceWithType'],
                                 'stringReplaceWith': replace_dict['stringReplaceWith'],
                                 'doubleReplaceWith': replace_dict['doubleReplaceWith'],
                                 'datetimeReplaceWith': replace_dict['datetimeReplaceWith'],
                                 'booleanReplaceWith': replace_dict['booleanReplaceWith'],
                                 'errorReplaceWith': error_replace_with
                             })

    def _raise_if_missing_secrets(self, secrets: Dict[str, str]=None):
        missing_secrets = set(self.get_missing_secrets())
        if len(missing_secrets) == 0:
            return

        new_secret_ids = set(secrets.keys()) if secrets else set()
        missing_secrets = missing_secrets.difference(new_secret_ids)

        if len(missing_secrets) == 0:
            return

        class MissingSecretsError(Exception):
            def __init__(self, missing_secret_ids):
                super().__init__(
                    'Required secrets are missing. Please call use_secrets to register the missing secrets.\n'
                    'Missing secrets:\n{}'.format('\n'.join(missing_secret_ids))
                )
                self.missing_secret_ids = missing_secret_ids

        raise MissingSecretsError(missing_secrets)

    # Steps are immutable so we don't need to create a full deepcopy of them when cloning Dataflows.
    def __deepcopy__(self, memodict=None):
        return copy(self)

    def __getitem__(self, key):
        if isinstance(key, slice):
            return Dataflow(self._engine_api, self._steps[key], self._name, self.id)
        else:
            raise TypeError("Invalid argument type.")

    # Will fold the right Dataflow into the left by appending the rights steps to the lefts.
    def __add__(self, other):
        if not isinstance(other, BaseDataflow):
            raise TypeError("Can only add two Dataflow objects together. Was given: " + str(type(other)))
        return Dataflow(self._engine_api,
                        self._steps + other._steps,
                        self._name,
                        self.id,
                        self.parent_package_path)

    def __repr__(self):
        # Get name property so that _name is filled if possible.
        self.name
        result = dedent("""\
        Dataflow
          name: {_name}
          parent_package_path: {_parent_package_path}
          steps: [\n""".format(**vars(self)))
        result += ''.join(
            indent(str(step), '  ' * 2) + ',\n'
            for step in self._steps)
        result += '  ]'
        return result

    @staticmethod
    def join(left_dataflow: DataflowReference,
             right_dataflow: DataflowReference,
             join_key_pairs: List[Tuple[str, str]] = None,
             join_type: JoinType = JoinType.MATCH,
             left_column_prefix: str = 'l_',
             right_column_prefix: str = 'r_',
             left_non_prefixed_columns: List[str] = None,
             right_non_prefixed_columns: List[str] = None) -> 'Dataflow':
        """
        Creates a new Dataflow that is a result of joining two provided Dataflows.

        :param left_dataflow: Left Dataflow or DataflowReference to join with.
        :param right_dataflow: Right Dataflow or DataflowReference to join with.
        :param join_key_pairs: Key column pairs. List of tuples of columns names where each tuple forms a key pair to
            join on. For instance: [('column_from_left_dataflow', 'column_from_right_dataflow')]
        :param join_type: Type of join to perform. Match is default.
        :param left_column_prefix: Prefix to use in result Dataflow for columns originating from left_dataflow.
            Needed to avoid column name conflicts at runtime.
        :param right_column_prefix: Prefix to use in result Dataflow for columns originating from right_dataflow.
            Needed to avoid column name conflicts at runtime.
        :param left_non_prefixed_columns: List of column names from left_dataflow that should not be prefixed with
            left_column_prefix. Every other column appearing in the data at runtime will be prefixed.
        :param right_non_prefixed_columns: List of column names from right_dataflow that should not be prefixed with
            left_column_prefix. Every other column appearing in the data at runtime will be prefixed.
        :return: The new Dataflow.
        """
        from .engineapi.api import get_engine_api
        from .references import make_activity_reference

        df = Dataflow(get_engine_api())
        return df.add_step('TwoWayJoin', {
            'leftActivityReference': left_dataflow if isinstance(left_dataflow, ActivityReference)
            else make_activity_reference(left_dataflow),
            'rightActivityReference': right_dataflow if isinstance(right_dataflow, ActivityReference)
            else make_activity_reference(right_dataflow),
            'joinKeyPairs': [{'leftKeyColumn': pair[0], 'rightKeyColumn': pair[1]} for pair in join_key_pairs],
            'joinType': join_type,
            'leftColumnPrefix': left_column_prefix,
            'rightColumnPrefix': right_column_prefix,
            'leftNonPrefixedColumns': left_non_prefixed_columns,
            'rightNonPrefixedColumns': right_non_prefixed_columns
        })
