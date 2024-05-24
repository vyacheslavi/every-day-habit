from dotenv import find_dotenv
from pathlib import Path
from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent.parent


class RunSettings(BaseModel):
    port: int = 8000
    host: str = "127.0.0.1"


class DBSettings(BaseModel):
    pg_dsn: PostgresDsn
    db_echo: bool = False


class SecuritySettings(BaseModel):
    jwt_private_key: Path = BASE_DIR / "backend" / "certs" / "jwt-private.pem"
    jwt_public_key: Path = BASE_DIR / "backend" / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=find_dotenv(".env"),
        env_file_encoding="utf-8",
        env_prefix="APP_CONFIG__",
        env_nested_delimiter="__",
    )

    db: DBSettings
    security: SecuritySettings = SecuritySettings()
    run: RunSettings = RunSettings()


settings = Settings()
