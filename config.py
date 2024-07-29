from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    repository_type: str = "sqlite"

    db_url: str = "sqlite:///./test.db"

    class Config:
        env_file = ".env"

settings = Settings()
