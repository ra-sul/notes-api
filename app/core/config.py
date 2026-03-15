import os

from pydantic import Field, ConfigDict
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENV: str = Field(default="dev")
    DEBUG: bool = Field(default=False)
    
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    DATABASE_URL: str

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        extra="ignore"
        )


settings = Settings()