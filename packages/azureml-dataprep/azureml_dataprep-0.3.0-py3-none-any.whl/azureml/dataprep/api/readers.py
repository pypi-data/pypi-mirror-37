# Copyright (c) Microsoft Corporation. All rights reserved.
from .builders import InferenceArguments, FileFormatBuilder
from .dataflow import Dataflow
from .datasources import FileDataSource, LocalDataSource, BlobDataSource, DataLakeDataSource, MSSQLDataSource
from ._datastore_helper import datastore_to_datasource
from .engineapi.typedefinitions import PromoteHeadersMode, SkipMode, FileEncoding
from .engineapi.api import get_engine_api
from .parseproperties import ParseParquetProperties
from typing import TypeVar, List
import re


FilePath = TypeVar('FilePath', FileDataSource, str)
blob_pattern = re.compile(r'^https://[^/]+\.blob\.core\.windows\.net', re.IGNORECASE)
adls_pattern = re.compile(r'^adl://[^/]+\.azuredatalake\.net', re.IGNORECASE)


def _datasource_from_str(value: str) -> FileDataSource:
    if blob_pattern.match(value):
        return BlobDataSource(value)
    elif adls_pattern.match(value):
        return DataLakeDataSource(value, 'token')
    else:
        return LocalDataSource(value)


def _datasource_from_path(path: FilePath) -> FileDataSource:
    if isinstance(path, FileDataSource):
        return path

    try:
        from azureml.data.abstract_datastore import AbstractDatastore
        from azureml.data.data_reference import DataReference

        if isinstance(path, DataReference) or isinstance(path, AbstractDatastore):
            return datastore_to_datasource(path)
    except ImportError:
        pass

    return _datasource_from_str(path)


def _default_skip_mode(skip_mode: SkipMode, skip_rows: int) -> SkipMode:
    return SkipMode.UNGROUPED if skip_rows > 0 and skip_mode == SkipMode.NONE else skip_mode


def read_csv(path: FilePath,
             separator: str = ',',
             header: PromoteHeadersMode = PromoteHeadersMode.CONSTANTGROUPED,
             encoding: FileEncoding = FileEncoding.UTF8,
             quoting: bool = False,
             inference_arguments: InferenceArguments = None,
             skip_rows: int = 0,
             skip_mode: SkipMode = SkipMode.NONE,
             comment: str = None,
             include_path: bool = False) -> Dataflow:
    """
    Creates a new Dataflow with the operations required to read and parse CSV data.

    :param path: The file(s) to load and parse.
    :param separator: The separator to use to split columns.
    :param header: How to determine column headers.
    :param encoding: The encoding of the files being read.
    :param quoting: Whether to handle new line characters within quotes. This option will impact performance.
    :param inference_arguments: Arguments that determine how data types are inferred.
    :param skip_rows: How many rows to skip.
    :param skip_mode: The mode in which rows are skipped.
    :param comment: Character used to indicate a line is a comment instead of data in the files being read.
    :param include_path: Whether to include a column containing the path from which the data was read.
    :return: A new Dataflow.
    """
    datasource = _datasource_from_path(path)
    skip_mode = _default_skip_mode(skip_mode, skip_rows)
    df = Dataflow.get_files(datasource)
    df = df.parse_delimited(separator, header, encoding, quoting, skip_rows, skip_mode, comment)

    if inference_arguments is not None:
        column_types_builder = df.builders.set_column_types()
        column_types_builder.learn(inference_arguments)
        df = column_types_builder.to_dataflow()

    if not include_path:
        df = df.drop_columns(['Path'])

    return df


def read_fwf(path: FilePath,
             offsets: List[int],
             header: PromoteHeadersMode = PromoteHeadersMode.CONSTANTGROUPED,
             encoding: FileEncoding = FileEncoding.UTF8,
             inference_arguments: InferenceArguments = None,
             skip_rows: int = 0,
             skip_mode: SkipMode = SkipMode.NONE,
             include_path: bool = False) -> Dataflow:
    """
    Creates a new Dataflow with the operations required to read and parse fixed-width data.

    :param path: The file(s) to load and parse.
    :param offsets: The offsets at which to split columns. The first column is always assumed to start at offset 0.
    :param header: How to determine column headers.
    :param encoding: The encoding of the files being read.
    :param inference_arguments: Arguments that determine how data types are inferred.
    :param skip_rows: How many rows to skip.
    :param skip_mode: The mode in which rows are skipped.
    :param include_path: Whether to include a column containing the path from which the data was read.
    :return: A new Dataflow.
    """
    datasource = _datasource_from_path(path)
    skip_mode = _default_skip_mode(skip_mode, skip_rows)
    df = Dataflow.get_files(datasource)
    df = df.parse_fwf(offsets, header, encoding, skip_rows, skip_mode)

    if inference_arguments is not None:
        column_types_builder = df.builders.set_column_types()
        column_types_builder.learn(inference_arguments)
        df = column_types_builder.to_dataflow()

    if not include_path:
        df = df.drop_columns(['Path'])

    return df


def read_excel(path: FilePath,
               sheet_name: str = None,
               use_header: bool = False,
               inference_arguments: InferenceArguments = None,
               skip_rows: int = 0,
               include_path: bool = False) -> Dataflow:
    """
    Creates a new Dataflow with the operations required to read Excel files.

    :param path: The file(s) to read.
    :param sheet_name: The name of the sheet to load.
    :param use_header: Whether to use the first row as column headers.
    :param inference_arguments: Arguments that determine how data types are inferred.
    :param skip_rows: How many rows to skip.
    :param include_path: Whether to include a column containing the path from which the data was read.
    :return: A new Dataflow.
    """
    datasource = _datasource_from_path(path)
    df = Dataflow.read_excel(datasource, sheet_name, use_header, skip_rows)

    if inference_arguments is not None:
        column_types_builder = df.builders.set_column_types()
        column_types_builder.learn(inference_arguments)
        df = column_types_builder.to_dataflow()

    if not include_path:
        df = df.drop_columns(['Path'])

    return df


def read_lines(path: FilePath,
               header: PromoteHeadersMode = PromoteHeadersMode.NONE,
               encoding: FileEncoding = FileEncoding.UTF8,
               skip_rows: int = 0,
               skip_mode: SkipMode = SkipMode.NONE,
               comment: str = None,
               include_path: bool = False) -> Dataflow:
    """
    Creates a new Dataflow with the operations required to read text files and split them into lines.

    :param path: The file(s) to read.
    :param header: How to determine column headers.
    :param encoding: The encoding of the files being read.
    :param skip_rows: How many rows to skip.
    :param skip_mode: The mode in which rows are skipped.
    :param comment: Character used to indicate a line is a comment instead of data in the files being read.
    :param include_path: Whether to include a column containing the path from which the data was read.
    :return: A new Dataflow.
    """
    datasource = _datasource_from_path(path)
    skip_mode = _default_skip_mode(skip_mode, skip_rows)
    df = Dataflow.get_files(datasource)
    df = df.parse_lines(header, encoding, skip_rows, skip_mode, comment)

    if not include_path:
        df = df.drop_columns(['Path'])

    return df


def detect_file_format(path: FilePath) -> FileFormatBuilder:
    """
    Analyzes the file(s) at the specified path and attempts to determine the type of file and the arguments required
    to read and parse it. The result is a FileFormatBuilder which contains the results of the analysis. This builder
    can be modified and used as the input to a new Dataflow.

    :param path: The file(s) to analyze.
    :return: A FileFormatBuilder.
    """
    datasource = _datasource_from_path(path)
    df = Dataflow.get_files(datasource)

    # File Format Detection
    ffb = df.builders.detect_file_format()
    ffb.learn()
    return ffb


def smart_read_file(path: FilePath, include_path: bool = False) -> Dataflow:
    """
    Analyzes the file(s) at the specified path and returns a new Dataflow containing the operations required to
    read and parse them. The type of the file and the arguments required to read it are inferred automatically.

    :param path: The file(s) to read.
    :param include_path: Whether to include a column containing the path from which the data was read.
    :return: A new Dataflow.
    """
    datasource = _datasource_from_path(path)
    df = Dataflow.get_files(datasource)

    # File Format Detection
    ffb = df.builders.detect_file_format()
    ffb.learn()
    df = ffb.to_dataflow(include_path=include_path)

    # Type Inference, except for parquet
    if type(ffb.file_format) != ParseParquetProperties:
        column_types_builder = df.builders.set_column_types()
        column_types_builder.learn()
        df = column_types_builder.to_dataflow()

    return df


def read_sql(data_source: MSSQLDataSource, query: str):
    """
    Creates a new Dataflow that can read data from an MS SQL database by executing the query specified.

    :param data_source: The details of the MS SQL database.
    :param query: The query to execute to read data.
    :return: A new Dataflow.
    """
    df = Dataflow(get_engine_api())
    df = df.read_sql(data_source, query)

    return df


def read_parquet_file(path: FilePath, include_path: bool = False):
    datasource = _datasource_from_path(path)
    df = Dataflow.get_files(datasource)
    df = df.read_parquet_file()

    if not include_path:
        df = df.drop_columns(['Path'])

    return df


def read_parquet_dataset(path: FilePath, include_path: bool = False):
    datasource = _datasource_from_path(path)
    df = Dataflow.read_parquet_dataset(datasource)

    if not include_path:
        df = df.drop_columns(['Path'])

    return df


def read_json(path: FilePath,
              encoding: FileEncoding = FileEncoding.UTF8,
              flatten_nested_arrays: bool = False,
              include_path: bool = False):
    datasource = _datasource_from_path(path)
    df = Dataflow.get_files(datasource)

    # Json format detection
    builder = df.builders.extract_table_from_json()
    builder.encoding = encoding
    builder.flatten_nested_arrays = flatten_nested_arrays
    builder.learn()
    df = builder.to_dataflow()

    if not include_path:
        df = df.drop_columns(['Path'])

    return df
