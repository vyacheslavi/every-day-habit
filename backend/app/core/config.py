from dotenv import find_dotenv
from pathlib import Path
from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent.parent


class RunSettings(BaseModel):
    scheme: str = "http"
    port: int = 8000
    host: str = "127.0.0.1"
    url: str = f"{scheme}://{host}:{port}"


class EmailSettings(BaseModel):
    login: str
    password: str


class DBSettings(BaseModel):
    pg_dsn: str
    db_echo: bool = False


class SecuritySettings(BaseModel):
    jwt_private_key: Path = BASE_DIR / "certs" / "jwt-private.pem"
    jwt_public_key: Path = BASE_DIR / "certs" / "jwt-public.pem"
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
    email: EmailSettings
    security: SecuritySettings = SecuritySettings()
    run: RunSettings = RunSettings()


settings = Settings()
