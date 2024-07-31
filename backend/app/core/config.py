from typing import Literal
from dotenv import find_dotenv
from pathlib import Path
from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent.parent


class CelerySettings(BaseModel):
    broker_url: str
    result_backend_url: str


class RunSettings(BaseModel):
    scheme: str = "http"
    port: int = 8000
    host: str = "0.0.0.0"
    url: str = "https://edh.vyacheslavi.ru"


class EmailSettings(BaseModel):
    login: str
    password: str


class DBSettings(BaseModel):
    pg_dsn: str
    echo: bool


class TestDBSettings(BaseModel):
    pg_dsn: str
    echo: bool


class SecuritySettings(BaseModel):
    jwt_private_key: Path = BASE_DIR / "certs" / "jwt-private.pem"
    jwt_public_key: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 60 * 24 * 3
    verification_token_expire_minutes: int = 10
    reset_token_expire_minutes: int = 10


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=find_dotenv(".env"),
        env_file_encoding="utf-8",
        env_prefix="APP_CONFIG__",
        env_nested_delimiter="__",
        extra="ignore",
    )
    mode: Literal["TEST", "DEV", "PROD"]
    db: DBSettings
    test_db: TestDBSettings
    email: EmailSettings
    security: SecuritySettings = SecuritySettings()
    celery: CelerySettings
    run: RunSettings = RunSettings()


settings = Settings()
