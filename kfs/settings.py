from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

load_dotenv()


class Settings(BaseSettings):
    """Application settings managed by pydantic-settings."""

    model_config = SettingsConfigDict(env_file=".env",
                                      env_file_encoding="utf-8",
                                      extra="allow",
                                      case_sensitive=True)

    # API Service
    BASE_URL: str = Field(default="http://127.0.0.1:8000")
    SERVICE_NAME: str = Field(default="KFS-API")
    SERVICE_DESCRIPTION: str = Field(default="API for searching journeys")
    VERSION: str = Field(default="1.0.0")
    DOCS_PATH: str = Field(default="/docs")
    OPENAPI_PATH: str = Field(default="/openapi.json")
    SEARCH_PATH: str = Field(default="/journeys/search")

    # Client API Configuration
    CLIENT_MODE: str = Field(default="API")  # Options: "API", "TEST"
    API_URL: str = Field(default="")

    # Time constraints
    MAX_JOURNEY_DURATION_HOURS: int = Field(default=24)
    MAX_CONNECTION_TIME_HOURS: int = Field(default=4)
    MIN_CONNECTION_TIME_HOURS: int = Field(default=0)

    # Max connections per journey (default: 1 connection, 2 flights)
    MAX_CONNECTIONS: int = Field(default=1)

    # Max events count for process with DFS strategy
    MAX_DFS_STRATEGY: int = Field(default=500)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.DOCS_URL = f"{self.BASE_URL}{self.DOCS_PATH}"
        self.OPENAPI_URL = f"{self.BASE_URL}{self.OPENAPI_PATH}"


settings = Settings()
