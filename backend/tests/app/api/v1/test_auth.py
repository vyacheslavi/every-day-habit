from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app import crud, schemas
from backend.app.api import tokens_helper
from backend.tests.support import token


class TestRegister:
    async def test_register_success(
        self,
        client: AsyncClient,
        session: AsyncSession,
    ):
        # Given
        body = {"email": "example@mail.ru", "password": "test_password"}
        headers = {
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        # When
        response = await client.post(
            url="/api/v1/registration", data=body, headers=headers
        )
        user = await crud.user.get_by_email(
            session=session,
            email=body["email"],
        )

        # Then
        assert response.status_code == 200
        assert user.email == body["email"]

    async def test_register_user_already_exist(
        self,
        client: AsyncClient,
    ):
        # Given
        body = {"email": "example@mail.ru", "password": "test_password"}
        headers = {
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        # When
        response = await client.post(
            url="/api/v1/registration", data=body, headers=headers
        )

        # Then
        assert response.status_code == 403


class TestVerificator:
    async def test_verificator(
        self,
        client: AsyncClient,
    ):
        user = schemas.UserCreate(email="example@mail.ru", password="test_password")
        token_dict = await tokens_helper.create_verification_token(user=user)

        # Given
        token = token_dict["token"]

        # When
        response = await client.post(url=f"/api/v1/login/verificator?token={token}")

        # Then
        assert response.status_code == 200

    async def test_verificator_invalid_token_exc(
        self,
        client: AsyncClient,
    ):
        # Given

        # When
        response = await client.post(
            url=f"/api/v1/login/verificator?token={token.EXPIRED_TOKEN}"
        )

        # Then
        assert response.status_code == 403


class TestLogin:
    async def test_login_token_issue(
        self,
        client: AsyncClient,
    ):
        body = {
            "grant_type": "password",
            "username": "example@mail.ru",
            "password": "test_password",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        }
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        # When
        response = await client.post(
            url="/api/v1/token",
            data=body,
            headers=headers,
        )

        assert response.status_code == 200

    async def test_login_token_issue(
        self,
        client: AsyncClient,
    ):
        body = {
            "grant_type": "password",
            "username": "example@mail.ru",
            "password": "wrong_password",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        }
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        # When
        response = await client.post(
            url="/api/v1/token",
            data=body,
            headers=headers,
        )

        assert response.status_code == 401
