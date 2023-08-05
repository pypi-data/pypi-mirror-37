# Copyright (c) Microsoft Corporation. All rights reserved.
# Here many parts of the DataPrep API are re-exported under the 'azureml.dataprep' namespace for convenience.

# extend_path searches all directories on sys.path for any packages that exists under the same namespace
# as __name__. This handles different modules from the same namespace being installed in different places.
# https://docs.python.org/3.6/library/pkgutil.html#pkgutil.extend_path
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

# Builders
from .api.builders import InferenceArguments, FileFormatArguments, SourceData, ImputeColumnArguments
from .api.engineapi.typedefinitions import ReplaceValueFunction, StringMissingReplacementOption

# Dataflow
from .api.dataflow import Dataflow, EndOfLineConvention
from .api.dataflow_generated import DataflowReference, ReplacementsValue, HistogramArgumentsValue, \
    KernelDensityArgumentsValue, SummaryColumnsValue, BaseDataflow

# Engine Types used by Dataflow
from .api.engineapi.typedefinitions import ColumnRelationship, DecimalMark, SummaryFunction, TrimType, \
    MismatchAsOption, AssertPolicy

# DataProfile
from .api.dataprofile import ColumnProfile, DataProfile, HistogramBucket, ValueCountEntry

# DataSources
from .api.datasources import Path, LocalDataSource, BlobDataSource, DatabaseAuthType, MSSQLDataSource, \
    LocalFileOutput, BlobFileOutput

# Expressions
from .api.expressions import col, f_not, f_and, f_or, cond, Expression, ExpressionLike, value

# Functions
from .api.functions import round, trim_string

# Package
from .api.package import Package, PackageArgs

# Parse Properties
from .api.parseproperties import ParseDelimitedProperties, ParseFixedWidthProperties, ParseLinesProperties, \
    ParseParquetProperties, ReadExcelProperties, ReadJsonProperties, ParseDatasourceProperties

# Readers
from .api.readers import FilePath, read_csv, read_fwf, read_excel, read_lines, read_sql, read_parquet_file, \
    read_parquet_dataset, read_json, detect_file_format, smart_read_file, SkipMode, PromoteHeadersMode, \
    FileEncoding, InferenceArguments

# References
from .api.references import ExternalReference

# Secret Manager
from .api.secretmanager import Secret, register_secrets, register_secret, create_secret

# Steps
from .api.step import ColumnSelector, MultiColumnSelection

# Type Conversions
from .api.typeconversions import FieldType, TypeConverter, DateTimeConverter, CandidateDateTimeConverter, \
    CandidateConverter, InferenceInfo

# Types
from .api.types import SplitExample, Delimiters
