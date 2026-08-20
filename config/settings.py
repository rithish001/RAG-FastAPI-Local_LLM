from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    OLLAMA_URL: str
    OLLAMA_MODEL: str

    CHROMA_DB_PATH: str
    COLLECTION_NAME: str


    TOP_K_RESULTS: int = 3

    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

settings = Settings()

