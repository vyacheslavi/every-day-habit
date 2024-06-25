from fastapi import HTTPException, status


unauth_exc = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid username or password",
)
inactive_exc = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="User inactive or not verified",
)
not_super_user_exc = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="User is not superuser",
)
token_or_user_invalid_exc = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Token invalid (user not found)",
)
token_invalid_exc = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Token invalid or expired",
)
user_already_exist = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="User with this name already exists",
)
too_large_goal = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Goal must be less or equal 30 days",
)
