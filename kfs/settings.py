from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

load_dotenv()


class Settings(BaseSettings):
    """Application settings managed by pydantic-settings."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="allow")

    CLIENT_MODE: str = Field(default="API", json_schema_extra={"env": "CLIENT_MODE"})  # Op:("API", "TEST")
    API_URL: str = Field(default="", json_schema_extra={"env": "API_URL"})
    SEARCH_URL_PATH: str = Field(default="/journeys/search", json_schema_extra={"env": "SEARCH_URL_PATH"})

    # Time constraints
    MAX_JOURNEY_DURATION_HOURS: int = Field(default=24, json_schema_extra={"env": "MAX_JOURNEY_DURATION_HOURS"})
    MAX_CONNECTION_TIME_HOURS: int = Field(default=4, json_schema_extra={"env": "MAX_CONNECTION_TIME_HOURS"})
    MIN_CONNECTION_TIME_HOURS: int = Field(default=0, json_schema_extra={"env": "MIN_CONNECTION_TIME_HOURS"})

    # Max connections per journey (default: 1 connection, 2 flights)
    MAX_CONNECTIONS: int = Field(default=1, json_schema_extra={"env": "MAX_CONNECTIONS"})

    # Rate Limiting Settings
    RATE_LIMIT: str = Field(default="10/minute", json_schema_extra={"env": "RATE_LIMIT"})


settings = Settings()
