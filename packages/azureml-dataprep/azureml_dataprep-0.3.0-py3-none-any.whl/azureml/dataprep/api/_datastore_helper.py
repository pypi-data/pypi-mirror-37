# Copyright (c) Microsoft Corporation. All rights reserved.
from .datasources import FileDataSource, BlobDataSource, DataLakeDataSource
from typing import TypeVar

DEFAULT_SAS_DURATION = 30 # this aligns with our SAS generation in the UI BlobStorageManager.ts
AML_INSTALLED = True
try:
    from azureml.data.abstract_datastore import AbstractDatastore
    from azureml.data.azure_storage_datastore import AbstractAzureStorageDatastore, AzureFileDatastore, \
                                                     AzureBlobDatastore
    from azureml.data.azure_data_lake_datastore import AzureDataLakeDatastore
    from azureml.data.data_reference import DataReference
except ImportError:
    AML_INSTALLED = False


DatastoreSource = TypeVar('DatastoreSource', 'AbstractDatastore', 'DataReference')


def datastore_to_datasource(data_source: DatastoreSource) -> FileDataSource:
    _ensure_imported()

    datastore = None
    path_on_storage = ''

    if isinstance(data_source, AbstractDatastore):
        datastore = data_source
    elif isinstance(data_source, DataReference):
        datastore = data_source.datastore
        path_on_storage = data_source.path_on_datastore or path_on_storage

    _ensure_supported(datastore)

    path_on_storage = path_on_storage.lstrip('/')
    if isinstance(datastore, AbstractAzureStorageDatastore):
        sas_token = _get_sas_token(datastore).lstrip('?')
        service = 'blob' if isinstance(datastore, AzureBlobDatastore) else 'file'
        url = '{}://{}.{}.{}/{}/{}?{}'.format(
            datastore.protocol,
            datastore.account_name,
            service,
            datastore.endpoint,
            datastore.container_name,
            path_on_storage,
            sas_token
        )
        return BlobDataSource(url)
    if isinstance(datastore, AzureDataLakeDatastore):
        # TODO: VSO #283878 Allow using service principal credentials for ADLS data sources
        access_token = _get_access_token(datastore)
        url = DataLakeDataSource.adl_template.format(datastore.store_name, path_on_storage)
        return DataLakeDataSource(url, accessToken=access_token)

    raise NotSupportedDatastoreTypeError(datastore)


def _ensure_imported():
    if not AML_INSTALLED:
        raise ImportError('Unable to import Azure Machine Learning SDK. In order to use datastore, please make ' \
                          + 'sure the Azure Machine Learning SDK is installed.')


def _ensure_supported(datastore: 'AbstractDatastore'):
    if isinstance(datastore, AzureFileDatastore):
        raise NotSupportedDatastoreTypeError(datastore)


def _get_sas_token(datastore: 'AbstractAzureStorageDatastore') -> str:
    if datastore.sas_token:
        return datastore.sas_token
    elif datastore.account_key:
        from azureml.vendor.azure_storage.common.cloudstorageaccount import CloudStorageAccount
        from datetime import datetime, timedelta

        account = CloudStorageAccount(datastore.account_name, account_key=datastore.account_key)
        expiry_date = datetime.utcnow() + timedelta(days=30)

        if isinstance(datastore, AzureFileDatastore):
            from azureml.vendor.azure_storage.file import FilePermissions

            service = account.create_file_service()
            return service.generate_share_shared_access_signature(
                share_name=datastore.container_name,
                permission=FilePermissions.READ,
                expiry=expiry_date
            )

        if isinstance(datastore, AzureBlobDatastore):
            from azureml.vendor.azure_storage.blob import ContainerPermissions

            service = account.create_block_blob_service()
            return service.generate_container_shared_access_signature(
                container_name=datastore.container_name,
                permission=ContainerPermissions(read=True, list=True),
                expiry=expiry_date
            )

        raise NotSupportedDatastoreTypeError(datastore)
    else:
        # public access
        return ''


def _get_access_token(datastore: 'AzureDataLakeDatastore') -> str:
    import adal # adal is a dependency of azureml-sdk not dataprep

    authority_url = '{}/{}'.format(datastore.authority_url, datastore.tenant_id)
    auth_context = adal.AuthenticationContext(authority=authority_url)
    token_obj = auth_context.acquire_token_with_client_credentials(
        resource=datastore.resource_url,
        client_id=datastore.client_id,
        client_secret=datastore.client_secret
    )
    return token_obj['accessToken']


class NotSupportedDatastoreTypeError(Exception):
    def __init__(self, datastore: 'AbstractDatastore'):
        super().__init__('Datastore "{}"\'s type "{}" is not supported.'.format(datastore.name, datastore.datastore_type))
        self.datastore = datastore
