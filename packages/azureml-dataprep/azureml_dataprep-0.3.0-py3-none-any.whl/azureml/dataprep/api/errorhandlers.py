# Copyright (c) Microsoft Corporation. All rights reserved.
# pylint: disable=line-too-long
error_messages = {
    'AccessDenied': 'You do not have permission to the specified path or file.',
    'SplitColumnProgramGenerationFailed': 'We were not able to split this column.',
    'ColumnInCustomBlockMissing': 'A column that does not exist was referenced in a custom code block.',
    'JSONReadError': 'Sorry, we were not able to open the requested JSON file. It is in a format that we could not understand. Please send us feedback about this file’s JSON structure.',
    'ReadFormatError': 'This data source cannot be parsed with the selected format.',
    'MismatchedHeaders': 'Column headers don\'t match between selected files',
    'MissingLeftKey': 'Join key column does not exist in the left source Dataflow.',
    'MissingLeftSource': 'The left source Dataflow does not exist.',
    'MissingRightKey': 'Join key column does not exist in the right source Dataflow.',
    'MissingRightSource': 'The right source Dataflow does not exist.',
    'DuplicateColumnName': 'Join will produce duplicate column names. Set the column name prefix.',
    'NothingToTrim': 'Trim String failed because nothing was chosen to trim.',
    'ReplaceNaValuesFailedNothingToReplace': 'Please provide the set of values that should be replaced.',
    'ReplaceValuesFailedNothingToReplace': 'Please provide a value to find.',
    'WrongEncodingWrite': 'The file could not be written using the specified encoding.',
    'InvalidSchema': 'The schema returned by the operation is not valid. Please ensure the resulting data frame contains only columns with no levels.',
    'OperatorRequiresValue': 'An operator in this filter is missing a value.',
    'UnknownDateFormat': 'The format of the date value specified was not in the correct format, YYYY-MM-DD.',
    'TargetColumnMissing': 'The target column is not present in the current data set.',
    'InvalidPath': 'The provided path is not valid.',
    'InvalidColumnName': 'The specified column name is not valid.',
    'ExpressionError': 'The provided expression failed with error: ',
    'ErrorInDependency': 'There is error in dependency Dataflow.',
    'UnknownExpressionError': 'The provided expression failed to be evaluated.',
    'WrongEncoding': 'The file could not be read using the specified encoding.',
    'Uncategorized': 'Could not execute the specified transform.',
    'BoolValuesConflict': 'Could not convert the same value to both True and False.',
    'DatabaseConnectionError': 'Could not connect to specified database.',
    'UnsupportedColumnType': 'Table contains unsupported column type (Variant).',
    'QueryExecutionError': 'Could not execute provided query.',
    'DatabaseLoginError': 'Login failed.',
    'DatabaseServerConnectionError': 'The server was not found or was not accessible.',
    'UnauthorizedAccess': 'Could not access the specified path due to permission or read-only properties.',
    'IOExceptionOnCreate': 'An I/O error occurred while creating the file with the specified path.',
    'PathTooLong': 'The specified path, file name, or both exceed the system-defined maximum length.',
    'FileOrDirectoryAlreadyExist': 'A file or directory with the same name already exists.',
    'FailedToExpandJson': 'The specified column could not be expanded. Check that column values are valid JSON.',
    'ReplaceRequiresValue': 'The Replace With field is missing a value, or choose to Replace With Nothing.',
    'ResourceCredentialsMissing': 'The required credentials to access this resource are missing. Please edit the block to re-enter them.',
    'AllLinesAreSkipped': 'All data rows are skipped.',
    'FailedToCacheData': 'Failed to generate a cache from the previous steps.',
    'FailedToSubmitSampleCacheRun': 'Submitting the sample job to your remote runner failed. Please verify the connection details and try again.',
    'FailedToDownloadSampleCache': 'Failed to download the remote sample cache to your local machine. Please ensure your local machine has access to the intermediate path or that you\'ve provided an appropriate SAS.',
    'SampleCacherMissing': 'The runner selected for this sample is missing from your system. Please select a different runner.',
    'SampleMissing': 'The specified sample is missing. Please refresh the sample to generate it again.',
    'SampleDisabled': 'The specified sample is disabled because it is not compatible with your data source. Please edit it and try again.',
    'CachingAborted': 'Caching has been aborted.',
    'ReplaceMissingRequiresSelector': 'You must choose at least one of the options to identify missing values.',
    'TrimStringRequiresLeadingOrTrailing': 'You must choose at least one option from Trim Leading and Trim Trailing.',
    'TrimStringCustomCannotBeEmpty': 'The Custom Trim Characters value cannot be empty or only whitespace.',
    'PythonPathInvalid': 'Cannot start a Python process with the path provided. Please provide a different Python path.',
    'FailedToReadCache': 'Cannot retrieve cache. Please refresh the cache to generate it again.',
    'FailedToWriteCache': 'Cannot write cache. Please check if the specified cache folder exists.',
    'CacheFolderPathMissing': 'No cache folder provided. Please provide a cache folder path in App Settings or in the Cache step.',
    'FieldConflictError': 'Duplicate field found for combined schema. Please ensure column names are unique.',
    'AssertionFailed': 'Assertion failed.'
}


def raise_engine_error(error_response):
    error_code = error_response['errorCode']
    if 'ActivityExecutionFailed' in error_code:
        raise ExecutionError(error_response)
    elif 'UnableToPreviewDataSource' in error_code:
        raise PreviewDataSourceError(error_response)
    else:
        raise UnexpectedError(error_response)


class ExecutionError(Exception):
    def __init__(self, error_response):
        super().__init__(error_messages[error_response['errorData']['errorCode']])


class PreviewDataSourceError(Exception):
    def __init__(self, error_response):
        super().__init__(error_messages[error_response['errorData']['blockError']])


class UnexpectedError(Exception):
    def __init__(self, error):
        self.error = error

