from datetime import datetime, timezone, timedelta

import bcrypt
from jwt import JWT, jwk_from_pem
from jwt.utils import get_int_from_datetime
from jwt.exceptions import JWTDecodeError

from backend.app.core.config import settings


jwt_inst = JWT()


class DecodeTokenException(Exception):
    code = 400
    error_code = "TOKEN__DECODE_ERROR"
    message = "token decode error"


def encode_jwt(
    payload: dict,
    private_key=settings.security.jwt_private_key,
    algorithm=settings.security.algorithm,
    expire_minutes: int = settings.security.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
) -> dict:
    to_encode = payload.copy()
    # now = datetime.datetime.now(datetime.datetime.utcnow)
    now = datetime.now(timezone.utc)

    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)

    to_encode.update(
        exp=get_int_from_datetime(expire),
        iat=get_int_from_datetime(now),
    )
    with open(private_key, "rb") as fh:
        encoded = jwt_inst.encode(
            to_encode,
            jwk_from_pem(fh.read()),
            alg=algorithm,
        )

        token_dict = {"token": encoded, "expire": expire}

        return token_dict


def decode_jwt(
    token: str | bytes = str,
    public_key: str = settings.security.jwt_public_key,
    algorithm: str = settings.security.algorithm,
) -> dict:
    with open(public_key, "rb") as fh:
        try:
            decoded = jwt_inst.decode(
                token,
                jwk_from_pem(fh.read()),
                algorithms=algorithm,
            )
        except JWTDecodeError:
            raise DecodeTokenException
        return decoded


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pw_bytes = password.encode()
    return bcrypt.hashpw(pw_bytes, salt)


def validate_password(
    password: str,
    hash_pw: bytes,
) -> bool:
    return bcrypt.checkpw(
        password.encode(),
        hash_pw,
    )
