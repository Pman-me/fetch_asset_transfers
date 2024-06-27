from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')
    API_KEY: Optional[str]
    CHAIN: Optional[str]
    PB_ADDR: Optional[str]
