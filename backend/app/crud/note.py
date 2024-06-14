from sqlalchemy import Result, desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.database.models import NoteModel, UserModel
from backend.app import schemas
from .base import CRUDBase


class NoteCRUD(CRUDBase[NoteModel, schemas.NoteCreate, schemas.NoteUpdate]):
    async def get_for_month(
        self,
        month: int,
        year: int,
        user: UserModel,
        session: AsyncSession,
    ) -> list[NoteModel] | None:
        stmt = (
            select(NoteModel)
            .where(
                (NoteModel.created_at_month == month)
                & (NoteModel.created_at_year == year)
                & (NoteModel.user_id == user.id)
            )
            .order_by(desc(NoteModel.created_at))
        )
        result: Result = await session.execute(stmt)
        notes = result.scalars().all()
        return list(notes)


note = NoteCRUD(NoteModel)
