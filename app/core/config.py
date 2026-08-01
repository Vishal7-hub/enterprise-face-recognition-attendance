from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str 
    APP_VERSION: str 
    DEBUG: bool = True
    DATABASE_URL: str
    UPLOAD_DIR: str = "uploads/employees"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )


settings = Settings()