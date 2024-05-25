from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Config(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    JWT_SECRET_KEY: str
    ALGORITHM: str
    DEBUG: bool
    model_config = SettingsConfigDict(env_file='.env')


@lru_cache
def get_config():
    return Config()


config = get_config()
