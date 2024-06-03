from typing import Annotated
from fastapi import Depends, Form
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    OAuth2AuthorizationCodeBearer,
)

from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.database.db_helper import db_helper
from backend.app import crud, schemas
from backend.app.database.models.user import UserModel
from . import security_utils
from . import exceptions


oauth2_scheme = security_utils.OAuth2PasswordBearerWithCookie(tokenUrl="/v1/token")


async def verify_user(
    user: UserModel,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    await crud.user.verify_user(session=session, user=user)


async def authenticate_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> UserModel | None:

    user: UserModel = await crud.user.get_by_email(
        email=form_data.username,
        session=session,
    )

    if not user:
        raise exceptions.unauth_exc

    if not security_utils.validate_password(
        password=form_data.password,
        hash_pw=user.hashed_password,
    ):
        raise exceptions.unauth_exc

    if not user.is_active:
        raise exceptions.inactive_exc

    return user


async def get_current_payload(token: str = Depends(oauth2_scheme)):
    try:
        payload = security_utils.decode_jwt(
            token=token,
        )
        return payload
    except Exception as e:
        raise exceptions.token_invalid_exc


async def get_current_auth_user(
    session: AsyncSession = Depends(db_helper.session_dependency),
    payload=Depends(get_current_payload),
):
    email = payload.get("email")
    user = await crud.user.get_by_email(
        session=session,
        email=email,
    )
    if not user:
        raise exceptions.token_invalid_exc
    return user


async def get_current_active_verified_auth_user(
    user: UserModel = Depends(get_current_auth_user),
):
    if user.is_active and user.is_verified:
        return user
    else:
        raise exceptions.inactive_exc


async def get_current_super_user(
    user: UserModel = Depends(get_current_active_verified_auth_user),
):
    if user.is_superuser:
        return user
    else:
        raise exceptions.not_super_user_exc
