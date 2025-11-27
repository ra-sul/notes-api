import os

from pydantic import Field, ConfigDict
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENV: str = Field(default="dev")
    DEBUG: bool = Field(default=False)
      
    DATABASE_URL: str

    model_config = ConfigDict(env_file=f".env.{os.getenv('ENV', 'dev')}", env_file_encoding='utf-8')


settings = Settings()