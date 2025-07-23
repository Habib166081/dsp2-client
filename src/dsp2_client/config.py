from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    DSP2 Client configuration loaded from environment variables or .env file.
    """
    base_url: str
    timeout: float = 10.0
    log_level: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="DSP2_",
        case_sensitive=False
    )

settings = Settings()
