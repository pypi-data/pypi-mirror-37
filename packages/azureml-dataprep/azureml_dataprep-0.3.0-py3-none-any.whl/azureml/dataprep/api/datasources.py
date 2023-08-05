# Copyright (c) Microsoft Corporation. All rights reserved.
from .engineapi.typedefinitions import (DataSourceTarget, AzureBlobResourceDetails, DataSourcePropertyValue,
                                        ResourceDetails, LocalResourceDetails, AzureDataLakeResourceDetails,
                                        Secret, OutputFilePropertyValue,
                                        OutputFileDestination)
from .secretmanager import register_secret, create_secret
from ._oauthToken import get_az_cli_tokens
from typing import TypeVar, List, Callable, cast
from urllib.parse import urlparse
from enum import Enum
import os


Path = TypeVar('Path', str, List[str])


def _extract_resource_details(path: Path, extractor: Callable[[str], ResourceDetails]) -> List[ResourceDetails]:
    return [extractor(path)] if isinstance(path, str) else path.map(extractor)


def _extract_local_resource_details(path: str) -> ResourceDetails:
    return cast(ResourceDetails, LocalResourceDetails(os.path.abspath(os.path.expanduser(path))))


def _extract_blob_resource_details(path: str) -> ResourceDetails:
    parts_list = urlparse(path)
    path = '{0}://{1}{2}'.format(*parts_list)
    query_string = parts_list.query or None
    if query_string:
        register_secret(value=query_string, id=path)
        resource_details = AzureBlobResourceDetails(path, create_secret(path))
    else:
        resource_details = AzureBlobResourceDetails(path)
    return cast(ResourceDetails, resource_details)


class FileDataSource:
    def __init__(self, value: DataSourcePropertyValue):
        self.underlying_value = value


class LocalDataSource(FileDataSource):
    def __init__(self, path: Path):
        resource_details = _extract_resource_details(path, _extract_local_resource_details)
        datasource_property = DataSourcePropertyValue(target=DataSourceTarget.LOCAL, resource_details=resource_details)
        super().__init__(datasource_property)


class BlobDataSource(FileDataSource):
    def __init__(self, path: Path):
        resource_details = _extract_resource_details(path, _extract_blob_resource_details)
        datasource_property = DataSourcePropertyValue(target=DataSourceTarget.AZUREBLOBSTORAGE,
                                                      resource_details=resource_details)
        super().__init__(datasource_property)

class DataLakeDataSource(FileDataSource):
    adl_template = 'adl://{}.azuredatalakestore.net/{}'

    def __init__(self, path: Path, accessToken: str = None, refreshToken: str = None, tenant: str = None):
        encodedToken = ''
        if accessToken is None and refreshToken is None:
            access, refresh = get_az_cli_tokens(tenant)
            encodedToken = DataLakeDataSource._encodeOAuthToken(access, refresh)
        else:
            encodedToken = DataLakeDataSource._encodeOAuthToken(accessToken, refreshToken)
        resource_details = _extract_resource_details(path, DataLakeDataSource._registerSecret(encodedToken))
        datasource_property = DataSourcePropertyValue(target=DataSourceTarget.AZUREDATALAKESTORAGE,
                                                      resource_details=resource_details)
        super().__init__(datasource_property)

    @staticmethod
    def _registerSecret(oauthToken: str) -> Callable[[str], ResourceDetails]:
        def _path_to_resource_details(path: str) -> ResourceDetails:
            register_secret(value=oauthToken, id=path)
            resource_details = AzureDataLakeResourceDetails(create_secret(path), path)
            return cast(ResourceDetails, resource_details)
        return _path_to_resource_details

    @staticmethod
    def _encodeOAuthToken(accessToken: str, refreshToken: str) -> str:
        if refreshToken is None:
            return accessToken
        else:
            return 'access:{0}|refresh:{1}'.format(accessToken, refreshToken)

class DatabaseAuthType(Enum):
    SERVER = 0
    WINDOWS = 1


class MSSQLDataSource:
    def __init__(self, server_name: str, database_name: str, user_name: str, password: Secret, trust_server: bool = True):
        self.server = server_name
        self.credentials_type = DatabaseAuthType.SERVER
        self.database = database_name
        self.userName = user_name
        self.password = password
        self.trustServer = trust_server


DataSource = TypeVar('DataSource', FileDataSource, MSSQLDataSource)


class FileOutput:
    def __init__(self, value: OutputFilePropertyValue):
        self.underlying_value = value


class LocalFileOutput(FileOutput):
    def __init__(self, path: Path):
        resource_details = _extract_resource_details(path, _extract_local_resource_details)
        output_file_value = OutputFilePropertyValue(target=OutputFileDestination.LOCAL,
                                                    resource_details=resource_details)
        super().__init__(output_file_value)


class BlobFileOutput(FileOutput):
    def __init__(self, path: Path):
        resource_details = _extract_resource_details(path, _extract_blob_resource_details)
        output_file_value = OutputFilePropertyValue(target=OutputFileDestination.AZUREBLOB,
                                                    resource_details=resource_details)
        super().__init__(output_file_value)
