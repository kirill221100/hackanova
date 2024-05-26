from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Config(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    DEBUG: bool
    model_config = SettingsConfigDict(env_file='.env')


@lru_cache
def get_config():
    return Config()


config = get_config()
