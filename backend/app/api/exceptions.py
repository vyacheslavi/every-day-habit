from fastapi import HTTPException, status


unauth_exc = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid username of password",
)
inactive_exc = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="User inactive or not verified",
)
not_super_user_exc = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="User is not superuser",
)
token_invalid_exc = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="token invalid (user not found)",
)
user_already_exist = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="User with this name already exists",
)
