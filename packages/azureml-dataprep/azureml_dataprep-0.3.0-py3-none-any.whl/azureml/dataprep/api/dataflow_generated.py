# Copyright (c) Microsoft Corporation. All rights reserved.
# This file is auto-generated. Do not modify.
from .engineapi import typedefinitions
from .engineapi.api import EngineAPI, get_engine_api
from .datasources import FileDataSource, FileOutput
from .references import make_activity_reference, ExternalReference
from .step import Step, MultiColumnSelection, column_selection_to_selector_value, single_column_to_selector_value
from .builders import Builders
from .sparkexecution import SparkExecutor
from typing import List, Dict, Any, Optional, TypeVar
from uuid import UUID, uuid4
from ... import dataprep


class ReplacementsValue:
    def __init__(self,
                 source_value: str,
                 target_value: Optional[str] = None):
        """
        :param source_value: The value to replace.
        :param target_value: The replacement value.
        """
        self.source_value = source_value
        self.target_value = target_value

    def _to_pod(self) -> Dict[str, Any]:
        return {
            'sourceValue': self.source_value,
            'targetValue': self.target_value,
        }


class HistogramArgumentsValue:
    def __init__(self,
                 histogram_bucket_count: int):
        """
        """
        self.histogram_bucket_count = histogram_bucket_count

    def _to_pod(self) -> Dict[str, Any]:
        return {
            'histogramBucketCount': self.histogram_bucket_count,
        }


class KernelDensityArgumentsValue:
    def __init__(self,
                 kernel_density_point_count: int,
                 kernel_density_bandwidth: float):
        """
        """
        self.kernel_density_point_count = kernel_density_point_count
        self.kernel_density_bandwidth = kernel_density_bandwidth

    def _to_pod(self) -> Dict[str, Any]:
        return {
            'kernelDensityPointCount': self.kernel_density_point_count,
            'kernelDensityBandwidth': self.kernel_density_bandwidth,
        }


class SummaryColumnsValue:
    def __init__(self,
                 column_id: str,
                 summary_function: typedefinitions.SummaryFunction,
                 summary_column_name: str,
                 histogram_arguments: Optional[HistogramArgumentsValue] = None,
                 kernel_density_arguments: Optional[KernelDensityArgumentsValue] = None,
                 quantiles: Optional[List[float]] = None):
        """
        :param column_id: Column to summarize.
        :param summary_function: Aggregation function to use.
        :param summary_column_name: Name of the column holding the aggregate values.
        """
        self.column_id = column_id
        self.summary_function = summary_function
        self.summary_column_name = summary_column_name
        self.histogram_arguments = histogram_arguments
        self.kernel_density_arguments = kernel_density_arguments
        self.quantiles = quantiles

    def _to_pod(self) -> Dict[str, Any]:
        return {
            'columnId': self.column_id,
            'summaryFunction': self.summary_function,
            'summaryColumnName': self.summary_column_name,
            'histogramArguments': self.histogram_arguments,
            'kernelDensityArguments': self.kernel_density_arguments,
            'quantiles': self.quantiles,
        }


class BaseDataflow:
    def __init__(self,
                 engine_api: EngineAPI,
                 steps: List[Step] = None,
                 name: str = None,
                 id: UUID = None,
                 parent_package_path: str = None):

        self.id = id if id is not None else uuid4()
        self._engine_api = engine_api
        self._steps = steps if steps is not None else []
        self._name = name
        self._parent_package_path = parent_package_path

        self.builders = Builders(self, engine_api)
        self._spark_executor = SparkExecutor(engine_api)

    def add_step(self,
                 step_type: str,
                 arguments: Dict[str, Any],
                 local_data: Dict[str, Any] = None) -> 'dataprep.Dataflow':
        new_step = Step(step_type, arguments, local_data)
        return dataprep.api.dataflow.Dataflow(self._engine_api,
                                              self._steps + [new_step],
                                              self._name,
                                              self.id,
                                              self._parent_package_path)

    @property
    def parent_package_path(self):
        return self._parent_package_path

    @staticmethod
    def get_files(path: FileDataSource) -> 'dataprep.Dataflow':
        """
        Expands the path specified by reading globs and files in folders and outputs one record per file found.

        :param path: The path or paths to expand.
        :return: A new Dataflow.
        """
        from .dataflow import Dataflow
        df = Dataflow(get_engine_api())
        return df.add_step('Microsoft.DPrep.GetFilesBlock', {
                               'path': path.underlying_value
                           })

    @staticmethod
    def reference(reference: 'DataflowReference') -> 'dataprep.Dataflow':
        from .dataflow import Dataflow
        df = Dataflow(get_engine_api())
        return df.add_step('Microsoft.DPrep.ReferenceBlock', {
                               'reference': make_activity_reference(reference)
                           })

    @staticmethod
    def read_excel(path: FileDataSource,
                   sheet_name: Optional[str] = None,
                   use_column_headers: bool = False,
                   skip_rows: int = 0) -> 'dataprep.Dataflow':
        """
        Reads the Excel file in the path specified and loads its data.

        :param path: The path to the Excel file.
        :param sheet_name: The name of the sheet to load. The first sheet is loaded if none is provided.
        :param use_column_headers: Whether to use the first row as column headers.
        :param skip_rows: Number of rows to skip when loading the data.
        :return: A new Dataflow.
        """
        from .dataflow import Dataflow
        df = Dataflow(get_engine_api())
        return df.add_step('Microsoft.DPrep.ReadExcelBlock', {
                               'path': path.underlying_value,
                               'sheetName': sheet_name,
                               'useColumnHeaders': use_column_headers,
                               'skipRows': skip_rows
                           })

    @staticmethod
    def read_parquet_dataset(path: FileDataSource) -> 'dataprep.Dataflow':
        from .dataflow import Dataflow
        df = Dataflow(get_engine_api())
        return df.add_step('Microsoft.DPrep.ReadParquetDatasetBlock', {
                               'path': path.underlying_value
                           })

    def map_column(self,
                   column: str,
                   new_column_id: str,
                   replacements: Optional[List[ReplacementsValue]] = None) -> 'dataprep.Dataflow':
        """
        Creates a new column where matching values in the source column have been replaced with the specified values.

        :param column: The source column.
        :param new_column_id: The name of the mapped column.
        :param replacements: The values to replace and their replacements.
        :return: The modified Dataflow.
        """
        return self.add_step('Microsoft.DPrep.MapColumnBlock', {
                                 'column': single_column_to_selector_value(column),
                                 'newColumnId': new_column_id,
                                 'replacements': [p._to_pod() for p in replacements] if replacements is not None else None
                             })

    def null_coalesce(self,
                      columns: List[str],
                      new_column_id: str) -> 'dataprep.Dataflow':
        """
        For each record, selects the first non-null value from the columns specified and uses it as the value of a new
        column.

        :param columns: The source columns.
        :param new_column_id: The name of the new column.
        :return: The modified Dataflow.
        """
        return self.add_step('Microsoft.DPrep.NullCoalesceBlock', {
                                 'columns': [single_column_to_selector_value(p) for p in columns],
                                 'newColumnId': new_column_id
                             })

    def extract_error_details(self,
                              column: str,
                              error_value_column: str,
                              extract_error_code: bool = False,
                              error_code_column: Optional[str] = None) -> 'dataprep.Dataflow':
        """
        Extracts the error details from error values into a new column.

        :param column: The source column.
        :param error_value_column: Name of a column to hold the original value of the error.
        :param extract_error_code: Whether to also extract the error code.
        :param error_code_column: Name of a column to hold the error code.
        :return: The modified Dataflow.
        """
        return self.add_step('Microsoft.DPrep.ExtractErrorDetailsBlock', {
                                 'column': single_column_to_selector_value(column),
                                 'errorValueColumn': error_value_column,
                                 'extractErrorCode': extract_error_code,
                                 'errorCodeColumn': error_code_column
                             })

    def duplicate_column(self,
                         column_pairs: Dict[str, str]) -> 'dataprep.Dataflow':
        """
        Creates new columns that are duplicates of the specified source columns.

        :param column_pairs: Mapping of the columns to duplicate to their new names.
        :return: The modified Dataflow.
        """
        return self.add_step('Microsoft.DPrep.DuplicateColumnBlock', {
                                 'columnPairs': [{'column': single_column_to_selector_value(k), 'newColumnId': v} for k, v in column_pairs.items()]
                             })

    def replace_na(self,
                   columns: MultiColumnSelection,
                   use_default_na_list: bool = True,
                   use_empty_string_as_na: bool = True,
                   use_nan_as_na: bool = True,
                   custom_na_list: Optional[str] = None) -> 'dataprep.Dataflow':
        """
        Replaces values in the specified columns with nulls. You can choose to use the default list, supply your own, or
        both.

        :param use_default_na_list: Use the default list and replace 'null', 'NaN', 'NA', and 'N/A' with null.
        :param use_empty_string_as_na: Replace empty strings with null.
        :param use_nan_as_na: Replace NaNs with Null.
        :param custom_na_list: Provide a comma separated list of values to replace with null.
        :param columns: The source columns.
        :return: The modified Dataflow.
        """
        return self.add_step('Microsoft.DPrep.ReplaceNaBlock', {
                                 'columns': column_selection_to_selector_value(columns),
                                 'useDefaultNaList': use_default_na_list,
                                 'useEmptyStringAsNa': use_empty_string_as_na,
                                 'useNanAsNa': use_nan_as_na,
                                 'customNaList': custom_na_list
                             })

    def trim_string(self,
                    columns: MultiColumnSelection,
                    trim_left: bool = True,
                    trim_right: bool = True,
                    trim_type: typedefinitions.TrimType = typedefinitions.TrimType.WHITESPACE,
                    custom_characters: str = '') -> 'dataprep.Dataflow':
        """
        Trims string values in specific columns.

        :param columns: The source columns.
        :param trim_left: Whether to trim from the beginning.
        :param trim_right: Whether to trim from the end.
        :param trim_type: Whether to trim whitespace or custom characters.
        :param custom_characters: The characters to trim.
        :return: The modified Dataflow.
        """
        return self.add_step('Microsoft.DPrep.TrimStringBlock', {
                                 'columns': column_selection_to_selector_value(columns),
                                 'trimLeft': trim_left,
                                 'trimRight': trim_right,
                                 'trimType': trim_type.value,
                                 'customCharacters': custom_characters
                             })

    def round(self,
              decimal_places: int,
              column: str) -> 'dataprep.Dataflow':
        """
        Rounds the values in the column specified to the desired number of decimal places.

        :param decimal_places: The number of decimal places.
        :param column: The source column.
        :return: The modified Dataflow.
        """
        return self.add_step('Microsoft.DPrep.RoundBlock', {
                                 'decimalPlaces': decimal_places,
                                 'column': single_column_to_selector_value(column)
                             })

    def clip(self,
             columns: MultiColumnSelection,
             lower: Optional[float] = None,
             upper: Optional[float] = None,
             use_values: bool = True) -> 'dataprep.Dataflow':
        """
        Clips values so that all values are between the lower and upper boundaries.

        :param columns: The source columns.
        :param lower: All values lower than this value will be set to this value.
        :param upper: All values higher than this value will be set to this value.
        :param use_values: If true, values outside boundaries will be set to the boundary values. If false, those values will be set to null.
        :return: The modified Dataflow.
        """
        return self.add_step('Microsoft.DPrep.ClipBlock', {
                                 'columns': column_selection_to_selector_value(columns),
                                 'lower': lower,
                                 'upper': upper,
                                 'useValues': use_values
                             })

    def str_replace(self,
                    columns: MultiColumnSelection,
                    value_to_find: Optional[str] = None,
                    replace_with: Optional[str] = None,
                    match_entire_cell_contents: bool = False,
                    use_special_characters: bool = False) -> 'dataprep.Dataflow':
        """
        Replaces values in a string column that match a search string with the specified value.

        :param columns: The source columns.
        :param value_to_find: The value to find.
        :param replace_with: The replacement value.
        :param match_entire_cell_contents: Whether the value to find must match the entire value.
        :param use_special_characters: If checked, you can use '#(tab)', '#(cr)', or '#(lf)' to represent special characters in the find or replace arguments.
        :return: The modified Dataflow.
        """
        return self.add_step('Microsoft.DPrep.StrReplaceBlock', {
                                 'columns': column_selection_to_selector_value(columns),
                                 'valueToFind': value_to_find,
                                 'replaceWith': replace_with,
                                 'matchEntireCellContents': match_entire_cell_contents,
                                 'useSpecialCharacters': use_special_characters
                             })

    def distinct_rows(self) -> 'dataprep.Dataflow':
        """
        Filters out records that contain duplicate values in all columns, leaving only a single instance.
        :return: The modified Dataflow.
        """
        return self.add_step('Microsoft.DPrep.DistinctRowsBlock', {
                             })

    def drop_nulls(self,
                   columns: MultiColumnSelection,
                   column_relationship: typedefinitions.ColumnRelationship = typedefinitions.ColumnRelationship.ALL) -> 'dataprep.Dataflow':
        """
        Drops rows where all or any of the selected columns are null.

        :param columns: The source columns.
        :param column_relationship: Whether all or any of the selected columns must be null.
        :return: The modified Dataflow.
        """
        return self.add_step('Microsoft.DPrep.DropNullsBlock', {
                                 'columns': column_selection_to_selector_value(columns),
                                 'columnRelationship': column_relationship.value
                             })

    def drop_errors(self,
                    columns: MultiColumnSelection,
                    column_relationship: typedefinitions.ColumnRelationship = typedefinitions.ColumnRelationship.ALL) -> 'dataprep.Dataflow':
        """
        Drops rows where all or any of the selected columns are an Error.

        :param columns: The source columns.
        :param column_relationship: Whether all or any of the selected columns must be an Error.
        :return: The modified Dataflow.
        """
        return self.add_step('Microsoft.DPrep.DropErrorsBlock', {
                                 'columns': column_selection_to_selector_value(columns),
                                 'columnRelationship': column_relationship.value
                             })

    def distinct(self,
                 columns: MultiColumnSelection) -> 'dataprep.Dataflow':
        """
        Filters out records that contain duplicate values in the specified columns, leaving only a single instance.

        :param columns: The source columns.
        :return: The modified Dataflow.
        """
        return self.add_step('Microsoft.DPrep.DistinctBlock', {
                                 'columns': column_selection_to_selector_value(columns)
                             })

    def skip(self,
             count: int) -> 'dataprep.Dataflow':
        """
        Skips the specified number of records.

        :param count: The number of records to skip.
        :return: The modified Dataflow.
        """
        return self.add_step('Microsoft.DPrep.SkipBlock', {
                                 'count': count
                             })

    def take(self,
             count: int) -> 'dataprep.Dataflow':
        """
        Takes the specified count of records.

        :param count: The number of records to take.
        :return: The modified Dataflow.
        """
        return self.add_step('Microsoft.DPrep.TakeBlock', {
                                 'count': count
                             })

    def rename_columns(self,
                       column_pairs: Dict[str, str]) -> 'dataprep.Dataflow':
        """
        Renames the specified columns.

        :param column_pairs: The columns to rename and the desired new names.
        :return: The modified Dataflow.
        """
        return self.add_step('Microsoft.DPrep.RenameColumnsBlock', {
                                 'columnPairs': [{'column': single_column_to_selector_value(k), 'newColumnId': v} for k, v in column_pairs.items()]
                             })

    def drop_columns(self,
                     columns: MultiColumnSelection) -> 'dataprep.Dataflow':
        """
        Drops the specified columns.

        :param columns: The source columns.
        :return: The modified Dataflow.
        """
        return self.add_step('Microsoft.DPrep.DropColumnsBlock', {
                                 'columns': column_selection_to_selector_value(columns)
                             })

    def keep_columns(self,
                     columns: MultiColumnSelection) -> 'dataprep.Dataflow':
        """
        Keeps the specified columns and drops all others.

        :param columns: The source columns.
        :return: The modified Dataflow.
        """
        return self.add_step('Microsoft.DPrep.KeepColumnsBlock', {
                                 'columns': column_selection_to_selector_value(columns)
                             })

    def promote_headers(self) -> 'dataprep.Dataflow':
        """
        Sets the first record in the dataset as headers, replacing any existing ones.
        :return: The modified Dataflow.
        """
        return self.add_step('Microsoft.DPrep.PromoteHeadersBlock', {
                             })

    def to_number(self,
                  columns: MultiColumnSelection,
                  decimal_point: typedefinitions.DecimalMark = typedefinitions.DecimalMark.DOT) -> 'dataprep.Dataflow':
        """
        Converts the values in the specified columns to floating point numbers.

        :param columns: The source columns.
        :param decimal_point: The symbol to use as the decimal mark.
        :return: The modified Dataflow.
        """
        return self.add_step('Microsoft.DPrep.ToNumberBlock', {
                                 'columns': column_selection_to_selector_value(columns),
                                 'decimalPoint': decimal_point.value
                             })

    def to_bool(self,
                columns: MultiColumnSelection,
                true_values: List[str],
                false_values: List[str],
                mismatch_as: typedefinitions.MismatchAsOption = typedefinitions.MismatchAsOption.ASFALSE) -> 'dataprep.Dataflow':
        """
        Converts the values in the specified columns to booleans.

        :param columns: The source columns.
        :param true_values: The values to treat as true.
        :param false_values: The values to treat as false.
        :param mismatch_as: How to treat values that don't match the values in the true or false values lists.
        :return: The modified Dataflow.
        """
        return self.add_step('Microsoft.DPrep.ToBoolBlock', {
                                 'columns': column_selection_to_selector_value(columns),
                                 'trueValues': [p for p in true_values],
                                 'falseValues': [p for p in false_values],
                                 'mismatchAs': mismatch_as.value
                             })

    def to_string(self,
                  columns: MultiColumnSelection) -> 'dataprep.Dataflow':
        """
        Converts the values in the specified columns to strings.

        :param columns: The source columns.
        :return: The modified Dataflow.
        """
        return self.add_step('Microsoft.DPrep.ToStringBlock', {
                                 'columns': column_selection_to_selector_value(columns)
                             })

    def to_long(self,
                columns: MultiColumnSelection) -> 'dataprep.Dataflow':
        """
        Converts the values in the specified columns to 64 bit integers.

        :param columns: The source columns.
        :return: The modified Dataflow.
        """
        return self.add_step('Microsoft.DPrep.ToLongBlock', {
                                 'columns': column_selection_to_selector_value(columns)
                             })

    def convert_unix_timestamp_to_datetime(self,
                                           columns: MultiColumnSelection,
                                           use_seconds: bool = False) -> 'dataprep.Dataflow':
        """
        Converts the specified column to DateTime values by treating the existing value as a Unix timestamp.

        :param columns: The source columns.
        :param use_seconds: Whether to use seconds as the resolution. Milliseconds are used if false.
        :return: The modified Dataflow.
        """
        return self.add_step('Microsoft.DPrep.ConvertUnixTimestampToDateTime', {
                                 'columns': column_selection_to_selector_value(columns),
                                 'useSeconds': use_seconds
                             })

    def summarize(self,
                  summary_columns: Optional[List[SummaryColumnsValue]] = None,
                  group_by_columns: Optional[List[str]] = None,
                  join_back: bool = False,
                  join_back_columns_prefix: Optional[str] = None) -> 'dataprep.Dataflow':
        """
        Summarizes data by running aggregate functions over specific columns. The aggregate functions are independent
        and it is possible to aggregate the same column multiple times. Unique names have to be provided for the
        resulting columns. The aggregations can be grouped, in which case one record is returned per group; or
        ungrouped, in which case one record is returned for the whole dataset. Additionally, the results of the
        aggregations can either replace the current dataset or augment it by appending the result columns.

        :param summary_columns: List of columns to summarize.
        :param group_by_columns: Columns to group by.
        :param join_back: Whether to append subtotals or replace current data with them.
        :param join_back_columns_prefix: Prefix to use for subtotal columns when appending them to current data.
        :return: The modified Dataflow.
        """
        return self.add_step('Microsoft.DPrep.SummarizeBlock', {
                                 'summaryColumns': [p._to_pod() for p in summary_columns] if summary_columns is not None else None,
                                 'groupByColumns': [p for p in group_by_columns] if group_by_columns is not None else None,
                                 'joinBack': join_back,
                                 'joinBackColumnsPrefix': join_back_columns_prefix
                             })

    def append_columns(self,
                       other_activities: List['DataflowReference']) -> 'dataprep.Dataflow':
        """
        Appends the columns from the referenced dataset to the current one. Duplicate columns will result in failure.

        :param other_activities: The source dataset.
        :return: The modified Dataflow.
        """
        return self.add_step('Microsoft.DPrep.AppendColumnsBlock', {
                                 'otherActivities': [make_activity_reference(p) for p in other_activities]
                             })

    def append_rows(self,
                    other_activities: List['DataflowReference']) -> 'dataprep.Dataflow':
        """
        Appends the records in the target dataset to the current one. If the schemas of the two datasets are distinct,
        this will result in records with different schemas.

        :param other_activities: The source dataset.
        :return: The modified Dataflow.
        """
        return self.add_step('Microsoft.DPrep.AppendRowsBlock', {
                                 'otherActivities': [make_activity_reference(p) for p in other_activities]
                             })

    def sort(self,
             sort_order: Dict[str, bool]) -> 'dataprep.Dataflow':
        """
        Sorts the dataset by the specified columns.

        :param sort_order: The columns to sort by and whether to sort ascending or descending. True is treated as descending, false as ascending.
        :return: The modified Dataflow.
        """
        return self.add_step('Microsoft.DPrep.SortBlock', {
                                 'sortOrder': [{'column': single_column_to_selector_value(k), 'descending': v} for k, v in sort_order.items()]
                             })

    def write_to_parquet(self,
                         file_path: Optional[FileOutput] = None,
                         directory_path: Optional[FileOutput] = None,
                         single_file: bool = False,
                         error: str = 'ERROR',
                         row_groups: int = 0) -> 'dataprep.Dataflow':
        """
        Writes out the data in the Dataflow into Parquet files.

        :param file_path: The path in which to store the output file.
        :param directory_path: The path in which to store the output files.
        :param error: String to use for error values.
        :param row_groups: Number of rows to use per row group.
        :return: The modified Dataflow.
        """
        return self.add_step('Microsoft.DPrep.WriteToParquetBlock', {
                                 'filePath': file_path.underlying_value if file_path is not None else None,
                                 'directoryPath': directory_path.underlying_value if directory_path is not None else None,
                                 'singleFile': single_file,
                                 'error': error,
                                 'rowGroups': row_groups
                             })


DataflowReference = TypeVar('DataflowReference', BaseDataflow, ExternalReference)

