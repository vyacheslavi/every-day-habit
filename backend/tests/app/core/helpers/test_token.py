import pytest
from backend.app.api import security_utils
from backend.tests.support.token import EXPIRED_TOKEN


def test_encode_and_decode_jwt():
    # Given
    payload: dict = {
        "sub": "user_1",
        "email": "example@gmail.com",
    }

    # When
    token = security_utils.encode_jwt(payload)

    # Then
    decoded_token: dict[str, str] = security_utils.decode_jwt(token["token"])

    assert decoded_token["sub"] == "user_1"


def test_decode_decode_error():
    # Given
    token = "invalid"

    # When, Then
    with pytest.raises(security_utils.DecodeTokenException):
        security_utils.decode_jwt(token=token)


def test_decode_expired_error():
    # Given
    token = EXPIRED_TOKEN

    # When, Then
    with pytest.raises(security_utils.DecodeTokenException):
        security_utils.decode_jwt(token)
