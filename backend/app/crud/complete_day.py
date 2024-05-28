from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDBase
from backend.app.database.models import CompleteDayModel
from backend.app.schemas import CompleteDay


class CompleteDaysCRUD(CRUDBase[CompleteDayModel, CompleteDay, CompleteDay]):

    async def get_for_month(
        month: int,
        year: int,
        habit_id: int,
        session: AsyncSession,
    ) -> list[CompleteDayModel] | None:
        stmt = select(CompleteDayModel).where(
            (CompleteDayModel.date_month == month)
            & (CompleteDayModel.date_year == year)
            & (CompleteDayModel.habit_id == habit_id)
        )

        return await list(session.scalars(stmt))

    async def delete(
        self, habit_id: int, date: datetime, session: AsyncSession
    ) -> None:
        stmt = select(CompleteDayModel).where(
            (CompleteDayModel.date == date) & (CompleteDayModel.habit_id == habit_id)
        )

        await session.execute(statement=stmt)
        await session.commit()


complete_day = CompleteDaysCRUD(CompleteDayModel)
