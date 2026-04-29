from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "API Local Innovasoft"
    api_base_url: str = "https://pruebareactjs.test-class.com/Api/"
    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_db: str = "managerclient"
    cors_origins: str = "*"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()