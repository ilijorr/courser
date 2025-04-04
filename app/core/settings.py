from functools import lru_cache
from pathlib import Path
from typing import Self 
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Only use this class to create classes which inherit it"""
    model_config = SettingsConfigDict(
            env_file=Path(__file__).resolve().parent.parent.parent / ".env",
            extra="ignore"
            )
    app_name: str = Field(alias="APP_NAME", default="Courser")
    environment: str = Field(alias="ENVIRONMENT", default="production")

class RelationalSettings(Settings):
    """Relational database settings"""
    name: str = Field(..., alias="DB_NAME", min_length=1)
    user: str = Field(..., alias="DB_USER", min_length=1)
    password: str = Field(..., alias="DB_PASSWORD", min_length=1)
    host: str = Field(alias="DB_HOST", min_length=1, default="localhost")
    port: str = Field(alias="DB_PORT", min_length=1, default="5432")

    model_config = SettingsConfigDict(
            env_prefix="DB_"
            )

    @property
    def url(self) -> str:
        return (
                f"postgresql+psycopg2://{self.user}:{self.password}@"
                f"{self.host}:{self.port}/{self.name}"
                )

class EmbeddingSettings(Settings):
    """Embedding model settings. Only meant to be inherited"""
    pass

class AzureEmbeddingSettings(EmbeddingSettings):
    """Azure embedding settings"""
    endpoint: str = Field(..., alias="AZURE_OPENAI_ENDPOINT")
    api_key: str = Field(..., alias="AZURE_OPENAI_API_KEY")
    api_version: str = Field(..., alias="AZURE_OPENAI_API_VERSION")

    model_config = SettingsConfigDict(
            env_prefix="AZURE_OPENAI"
            )

class VectorSettings(Settings):
    """Vector database settings. Only meant to be inherited"""
    pass

class PineconeSettings(VectorSettings):
    """Pinecone index settings"""
    api_key: str = Field(..., alias="PINECONE_API_KEY")
    index_name: str = Field(..., alias="PINECONE_INDEX_NAME")

    model_config = SettingsConfigDict(
            env_prefix="PINECONE_"
            )

class SettingsFactory:
    @classmethod
    @lru_cache(maxsize=None)
    def create(cls, settings_class: type[Self]) -> Self:
        return settings_class()
