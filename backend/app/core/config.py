from dotenv import find_dotenv
from pathlib import Path
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=find_dotenv(".env"),
        env_file_encoding="utf-8",
    )

    pg_dsn: PostgresDsn
    jwt_private_key: Path = BASE_DIR / "backend" / "certs" / "jwt-private.pem"
    jwt_public_key: Path = BASE_DIR / "backend" / "certs" / "jwt-public.pem"

    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15


settings = Settings()


print(settings.model_dump())
