from langchain_openai import AzureOpenAIEmbeddings

from core.settings import AzureEmbeddingSettings, SettingsFactory

settings = SettingsFactory.create(AzureEmbeddingSettings)
def get_embeddings() -> AzureOpenAIEmbeddings:
    return AzureOpenAIEmbeddings(
            azure_endpoint=settings.endpoint,
            api_key=settings.api_key,
            api_version=settings.api_version
            )
