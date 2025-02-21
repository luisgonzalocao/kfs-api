from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

load_dotenv()


class Settings(BaseSettings):
    """Application settings managed by pydantic-settings."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="allow")

    CLIENT_MODE: str = Field(default="API")
    API_URL: str = Field(default="")

    # Configurable time constraints
    MAX_JOURNEY_DURATION_HOURS: int = Field(default=24)
    MAX_CONNECTION_TIME_HOURS: int = Field(default=4)
    MIN_CONNECTION_TIME_HOURS: int = Field(default=0)

    # Max connections per journey (default: 1 connection, 2 flights)
    MAX_CONNECTIONS: int = Field(default=1)


settings = Settings()
