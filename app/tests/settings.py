from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class TestSettings(BaseSettings):
    """Only use this class to create classes which inherit it"""
    model_config = SettingsConfigDict(
            env_file=Path(__file__).resolve().parent.parent.parent / ".env.test",
            extra="ignore",
            env_prefix="TEST_"
            )
   
    name: str = Field(..., alias="TEST_NAME", min_length=1)
    user: str = Field(..., alias="TEST_USER", min_length=1)
    password: str = Field(..., alias="TEST_PASSWORD", min_length=1)
    host: str = Field(alias="TEST_HOST", min_length=1, default="localhost")
    port: str = Field(alias="TEST_PORT", min_length=1, default="5432")

    @property
    def url(self) -> str:
        return (
                f"postgresql+psycopg2://{self.user}:{self.password}@"
                f"{self.host}:{self.port}/{self.name}"
                )

