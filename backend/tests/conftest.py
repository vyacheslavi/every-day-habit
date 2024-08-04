import os
import fastapi
import httpx
import pytest

from backend.app.database.models import Base
from backend.app.database.db_helper import test_db_helper, db_helper

from backend.app.database.models.user import UserModel
from main import initialize_backend_application

TEST_USER_EMAIL = "test@mail.com"
TEST_USER_PWD = "12345"


@pytest.fixture(name="backend_test_app")
def backend_test_app() -> fastapi.FastAPI:
    """
    A fixture that re-initializes the FastAPI instance for test application.
    """

    return initialize_backend_application()


@pytest.fixture(scope="session", autouse=True)
async def prepare_db():

    async with test_db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture
async def session():
    async with test_db_helper.session_factory() as session:
        yield session


@pytest.fixture(name="client", scope="function")
async def client(
    backend_test_app: fastapi.FastAPI,
) -> httpx.AsyncClient:  # type: ignore

    backend_test_app.dependency_overrides[db_helper.session_dependency] = (
        test_db_helper.session_dependency
    )

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=backend_test_app),
        base_url="http://testserver",
        headers={"Content-Type": "application/json"},
    ) as client:
        yield client


@pytest.fixture(name="auth_client", scope="function")
async def auth_client(
    client: httpx.AsyncClient,
):
    body = {
        "grant_type": "password",
        "username": TEST_USER_EMAIL,
        "password": TEST_USER_PWD,
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
    print(f"{response.text}--------------------------52------------------")
    access_token = response.cookies.get("access_token")
    client.cookies.set("access_token", access_token)
    print(f"{access_token}--------------------------53------------------")
    yield client
