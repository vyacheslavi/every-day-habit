from fastapi import APIRouter, Depends, Form, Response
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.database.db_helper import db_helper
from backend.app.database.models.user import UserModel
from backend.app.api import tokens_helper, deps, exceptions, security_utils
from backend.app import schemas, crud
from backend.celery_task.tasks.email_send import (
    send_verification_email,
    send_reset_password_email,
)

TYPE_ACCESS_TOKEN = "access"
TYPE_RESET_PASSWORD_TOKEN = "reset_password"
TYPE_VERIFICATION_TOKEN = "verification"


class Token(BaseModel):
    access_token: str
    # kind_of_token: str
    token_type: str = "Bearer"


router = APIRouter(
    tags=["Authentication/Registration"],
)


@router.post("/registration")
async def registration(
    user_in: schemas.UserCreate = Depends(schemas.UserCreate.as_form),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    user = await crud.user.create(user_in, session)

    if not user:
        raise exceptions.user_already_exist


@router.post("/login/verificator/request-on-verify")
async def send_verification_token(
    user_in: schemas.UserCreate = Depends(schemas.UserCreate.as_form),
):
    verification_token = await tokens_helper.create_verification_token(user=user_in)
    send_verification_email.delay(
        user_in.email,
        verification_token["token"],
    )


@router.post("/login/verificator")
async def user_verification(
    token: str,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    try:
        payload = security_utils.decode_jwt(token)
    except security_utils.DecodeTokenException:
        raise exceptions.token_invalid_exc
    email = payload["email"]
    user = await crud.user.get_by_email(email=email, session=session)
    await crud.user.verify_user(session=session, user=user)


@router.post(
    "/token",
    response_model=Token,
)
async def auth_user_issue_jwt(
    response: Response,
    user: UserModel = Depends(deps.authenticate_user),
) -> Token:
    token_dict = await tokens_helper.create_access_token(user)
    token = token_dict.get("token")
    response.set_cookie(
        key="access_token",
        value=f"Bearer {token}",
        expires=token_dict.get("expire"),
        httponly=True,
        samesite="strict",
    )
    return Token(
        access_token=token,
    )


@router.post("/login/reminder")
async def forgot_password(
    email: EmailStr = Form(...),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    user = await crud.user.get_by_email(
        session=session,
        email=email,
    )
    if not user:
        raise exceptions.user_not_exist

    reset_token = await tokens_helper.create_reset_password_token(email=email)
    send_reset_password_email.delay(
        email,
        reset_token["token"],
    )


@router.patch(
    "/login/recover",
)
async def user_reset_password(
    token: str = Form(...),
    password: str = Form(...),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    try:
        payload = security_utils.decode_jwt(token)
        email = payload["email"]
        await crud.user.change_password(
            email=email,
            password=password,
            session=session,
        )
    except security_utils.DecodeTokenException:
        raise exceptions.token_invalid_exc


@router.get("/user/me/", response_model=schemas.UserResponseModel)
async def auth_user_check_self_info(
    user: UserModel = Depends(deps.get_current_active_verified_auth_user),
):
    return user
