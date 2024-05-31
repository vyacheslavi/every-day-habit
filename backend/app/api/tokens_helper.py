from typing import NewType
from backend.app.api import security_utils
from backend.app.database.models import UserModel
from backend.app import schemas

Minutes = NewType("Minutes", int)


def create_token(
    payload: dict,
    expire_timedelta: Minutes = None,
) -> str:
    return security_utils.encode_jwt(
        payload=payload,
        expire_timedelta=expire_timedelta,
    )


async def create_access_token(user: UserModel) -> str:
    payload: dict = {
        "sub": user.email,
        "email": user.email,
    }
    return create_token(payload)


async def create_reset_password_token(user: UserModel) -> str:
    payload = {
        "email": user.email,
    }

    return create_token(payload)


async def create_verification_token(user: schemas.UserCreate) -> str:
    payload = {"verification": "OK", "email": user.email}
    return create_token(payload)
