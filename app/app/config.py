from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)
from pathlib import Path

BASE_URL = Path(__file__).parent.parent


class AppConfig(BaseModel):
    allowed_hosts: str
    secret_key: str


class DatabaseConfig(BaseModel):
    engine: str
    name: str
    user:str
    password: str
    host:str
    port: int


class SMTPConfig(BaseModel):
    email_host: str
    email_port: int
    email_host_user: str
    email_host_password: str
    email_use_ssl: bool


class SettingsApp(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(BASE_URL / ".env.template", BASE_URL / ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
    )
    app: AppConfig
    db: DatabaseConfig
    smtp: SMTPConfig


settings_app = SettingsApp()