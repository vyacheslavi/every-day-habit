import os
import asyncio
import fastapi
import httpx
import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker

from backend.app.database.models import Base
from backend.app.database.db_helper import test_db_helper, db_helper


from main import initialize_backend_application


@pytest.fixture(name="backend_test_app")
def backend_test_app() -> fastapi.FastAPI:
    """
    A fixture that re-initializes the FastAPI instance for test application.
    """

    return initialize_backend_application()


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


@pytest.fixture(scope="session", autouse=True)
async def prepare_db():

    async with test_db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="function")
async def session():
    async with test_db_helper.session_factory() as session:
        yield session


# @pytest.fixture(scope="session")
# def event_loop(request):
#     """Create an instance of the default event loop for each test case."""
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()
