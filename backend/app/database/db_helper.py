import os
from typing import AsyncGenerator
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

from backend.app.core.config import settings


class DataBaseHelper:

    def __init__(self, url, echo, params) -> None:
        self.engine = create_async_engine(
            url=url,
            echo=echo,
            **params,
        )

        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def session_dependency(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session


# if os.getenv("APP_CONFIG__MODE") == "TEST":
#     url = settings.test_db.pg_dsn
#     echo = settings.test_db.echo
#     params = {"poolclass": NullPool}
# else:
#     url = settings.db.pg_dsn
#     echo = settings.db.echo
#     params = {}


db_helper = DataBaseHelper(
    url=settings.db.pg_dsn,
    echo=settings.db.echo,
    params={},
)

test_db_helper = DataBaseHelper(
    url=settings.test_db.pg_dsn,
    echo=settings.test_db.echo,
    params={"poolclass": NullPool},
)
