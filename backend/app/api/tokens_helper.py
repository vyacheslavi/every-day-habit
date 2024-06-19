from datetime import timedelta
from typing import Dict, NewType, Optional

from backend.app.api import security_utils
from backend.app.database.models import UserModel
from backend.app import schemas
from backend.app.core.config import settings


def create_token(
    payload: dict,
    expire_timedelta: timedelta = None,
) -> dict:
    return security_utils.encode_jwt(
        payload=payload,
        expire_timedelta=expire_timedelta,
    )


async def create_access_token(user: UserModel) -> dict:
    payload: dict = {
        "sub": user.email,
        "email": user.email,
    }
    return create_token(payload)


async def create_reset_password_token(user: UserModel) -> dict:
    payload = {
        "email": user.email,
    }

    return create_token(
        payload,
        expire_timedelta=timedelta(
            minutes=settings.security.reset_token_expire_minutes
        ),
    )


async def create_verification_token(user: schemas.UserCreate) -> dict:
    payload = {"verification": "OK", "email": user.email}
    return create_token(
        payload,
        expire_timedelta=timedelta(
            minutes=settings.security.verification_token_expire_minutes
        ),
    )
