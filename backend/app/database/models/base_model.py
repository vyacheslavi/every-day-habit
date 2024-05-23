import asyncio
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)


# engine = create_async_engine(
#     url="postgresql+asyncpg://postgres:postgerdapost135@localhost/daily-habit",
#     echo=True,
# )


# async def init_models():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)


# asyncio.run(init_models())
