from typing import Any, Generic, List, Optional, TypeVar, Union, Tuple, Dict, NewType

from pydantic import BaseModel
from sqlalchemy import update
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession

ObjectId = NewType("ObjectId", int)
DBModelType = TypeVar("DBModelType", bound=DeclarativeBase)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[DBModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, db_model: DBModelType) -> None:
        """
        CRUD object with default methods create, read, update and delete
        """

        self.db_model = db_model

    async def get_by_id(
        self,
        id: ObjectId,
        session: AsyncSession,
    ) -> DBModelType | None:
        return await session.get(self.db_model, id)

    # async def get(
    #     self,
    #     id: ObjectId,
    #     session: AsyncSession,
    # ) -> DBModelType | None:
    #     return await session.get(DBModelType, id)

    async def create(
        self,
        document_in: CreateSchemaType,
        session: AsyncSession,
    ) -> DBModelType:
        try:
            document_to_db = self.db_model(**document_in.model_dump())
            session.add(document_to_db)
            await session.commit()
            return True
        except:
            return False

    async def update(
        self,
        id: ObjectId,
        document_in: UpdateSchemaType,
        session: AsyncSession,
    ) -> None:

        document_from_db = await self.get_by_id(id, session)
        documents_dict = document_in.model_dump(exclude_unset=True).items
        print(documents_dict)
        for key, value in documents_dict:
            setattr(document_from_db, key, value)

        update(self.db_model).values()

        await session.commit()

    async def delete(
        self,
        id,
        session: AsyncSession,
    ) -> bool:
        try:
            document_from_db = await self.get_by_id(id, session)
            await session.delete(document_from_db)
            await session.commit()
            return True
        except:
            return False
