from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

load_dotenv()


class Settings(BaseSettings):
    """Application settings managed by pydantic-settings."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="allow", case_sensitive=True)

    # API Metadata
    BASE_URL: str = Field(default="http://127.0.0.1:8000")
    VERSION: str = Field(default="1.0.0")

    # Client & API Configuration
    CLIENT_MODE: str = Field(default="API")  # Options: "API", "TEST"
    API_URL: str = Field(default="")
    SEARCH_URL_PATH: str = Field(default="/journeys/search")

    # Time constraints
    MAX_JOURNEY_DURATION_HOURS: int = Field(default=24)
    MAX_CONNECTION_TIME_HOURS: int = Field(default=4)
    MIN_CONNECTION_TIME_HOURS: int = Field(default=0)

    # Max connections per journey (default: 1 connection, 2 flights)
    MAX_CONNECTIONS: int = Field(default=1)

    # Max events count for process with DFS strategy
    MAX_DFS_STRATEGY: int = Field(default=500)


settings = Settings()
