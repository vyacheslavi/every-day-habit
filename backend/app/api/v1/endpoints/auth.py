from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from backend.app.database.db_helper import db_helper
from backend.app.database.models.user import UserModel
from backend.app.api import tokens_helper, deps, exceptions, security_utils
from backend.app.api.email_sender import email_sender
from backend.app import schemas, crud

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
    user_in: schemas.UserCreate,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    user = await crud.user.create(user_in, session)

    if user:
        verification_token = await tokens_helper.create_verification_token(user=user)
        await email_sender.send_request_on_verify(
            user.email,
            verification_token,
        )
    else:
        raise exceptions.user_already_exist


@router.get("/login/verificator")
async def user_verification(
    token: str, session: AsyncSession = Depends(db_helper.session_dependency)
):
    try:
        payload = security_utils.decode_jwt(token)
        email = payload["email"]
        user = await crud.user.get_by_email(email=email, session=session)
        await crud.user.verify_user(session=session, user=user)
        return "Successfull verification"
    except:
        raise "token invalid"


@router.post(
    "/token",
    response_model=Token,
)
async def auth_user_issue_jwt(
    user: UserModel = Depends(deps.authenticate_user),
) -> Token:
    token = await tokens_helper.create_access_token(user)
    return Token(
        access_token=token,
    )


@router.patch(
    "/login/recover",
)
async def user_reset_password(
    password: str = Form(...),
    user: UserModel = Depends(deps.get_current_active_verified_auth_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
):

    result = await crud.user.change_password(
        password=password,
        session=session,
        user=user,
    )
    return result


@router.get("/login/reminder")
async def forgot_password(email: EmailStr):
    pass


@router.get("/user/me/", response_model=schemas.UserResponseModel)
async def auth_user_check_self_info(
    user: UserModel = Depends(deps.get_current_active_verified_auth_user),
):
    return user
