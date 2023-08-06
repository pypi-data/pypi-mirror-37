from cloud_scanner_azure.config.azure_storage_config import AzureStorageConfig


class AzureCosmosDbConfig:
    """Configuration required for use of Azure CosmosDB provider."""

    def __init__(self, table_name, storage: AzureStorageConfig):
        self.account_name = storage.account_name
        self.account_key = storage.account_key
        self.table_name = table_name
