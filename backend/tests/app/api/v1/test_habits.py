from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app import crud, schemas
from backend.app.api import security_utils, tokens_helper
from backend.app.database.models.user import UserModel
from backend.tests.conftest import TEST_USER_EMAIL, TEST_USER_PWD
from backend.tests.support import token


async def test_user(
    session: AsyncSession,
):
    hash_pw: bytes = security_utils.hash_password(TEST_USER_PWD)
    session.add(
        UserModel(
            email=TEST_USER_EMAIL,
            hashed_password=hash_pw,
            is_verified=True,
        )
    )
    await session.commit()


async def test_habit_create(
    session: AsyncSession,
    auth_client: AsyncClient,
):
    # Given
    body = {
        "name": "habit1",
        "goal": "30",
        "created_at": "2024-08-03",
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }

    # When
    response = await auth_client.post(
        url="/api/v1/habits/",
        json=body,
        headers=headers,
        follow_redirects=True,
    )
    habit = await crud.habit.get_by_id(
        1,
        session=session,
    )
    print(
        f"{response.text}--------------------------------------------------------------------------------------------"
    )

    # Then
    assert response.status_code == 200
    assert habit.name == body["name"]
