from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str

    FILE_ALLOWED_TYPES: list
    FILE_DEFAULT_CHUNK_SIZE: int 

    MONGODB_URL: str
    MONGODB_DATABASE: str


    VECTOR_DB_BACKEND : str
    VECTOR_DB_PATH : str
    VECTOR_DB_DISTANCE_METHOD: str = None
    
    class Config:
        env_file = ".env"


def get_settings():
    return Settings()
