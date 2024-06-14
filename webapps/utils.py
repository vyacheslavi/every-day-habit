from fastapi import Request, HTTPException, status
from jwt.exceptions import JWSDecodeError
from backend.app import crud
from backend.app.api import security_utils
from backend.app.database.models.user import UserModel


async def get_user_via_request(request: Request, session) -> UserModel | None:
    token = request.cookies.get("access_token")
    if token:
        token = token.split(" ")[1]
        try:
            payload = security_utils.decode_jwt(token=token)
        except JWSDecodeError:
            return None
        email = payload.get("email")
        user = await crud.user.get_by_email(session=session, email=email)
        return user
    else:
        None
