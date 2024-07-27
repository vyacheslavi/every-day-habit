from typing import Union
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDBase
from backend.app.database.models import UserModel
from backend.app.schemas import UserCreate, UserUpdate
from backend.app.api import security_utils


class UserCRUD(CRUDBase[UserModel, UserCreate, UserUpdate]):

    async def get_by_email(
        self,
        session: AsyncSession,
        email: Union[str, EmailStr],
    ) -> UserModel | None:
        stmt = select(UserModel).where(UserModel.email == email)

        return await session.scalar(stmt)

    async def verify_user(
        self,
        session: AsyncSession,
        user: UserModel,
    ):
        user.is_verified = True
        await session.commit()

    async def create(self, document_in: UserCreate, session: AsyncSession) -> UserModel:
        user_exist = await self.get_by_email(session, document_in.email)
        if not user_exist:
            hash_pw: bytes = security_utils.hash_password(document_in.password)
            user: UserModel = UserModel(
                **document_in.model_dump(exclude={"password"}),
                hashed_password=hash_pw,
            )
            session.add(user)
            await session.commit()

            return document_in
        else:
            return None

    async def change_password(
        self, email: str, password: str, session: AsyncSession
    ) -> bool:
        user = await self.get_by_email(email=email, session=session)
        try:
            hash_pw: bytes = security_utils.hash_password(password)
            setattr(user, "hashed_password", hash_pw)
            session.add(user)
            await session.commit()
        except Exception:
            return False
        return True


user = UserCRUD(UserModel)
