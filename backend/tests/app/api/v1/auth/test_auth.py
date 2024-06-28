from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app import crud


class TestRegister:
    async def test_register(
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
        print(client, type(client))
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

    # async def test_request_on_verification():
    #     pass

    # async def test_verification():
    #     pass
