import datetime
import calendar

from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.database.models import UserModel, HabitModel
from backend.app import schemas
from .base import CRUDBase


class HabitCRUD(CRUDBase[HabitModel, schemas.HabitCreate, schemas.HabitUpdate]):
    async def get_all_from_user(
        self,
        user: UserModel,
        session: AsyncSession,
    ) -> list[HabitModel] | None:
        stmt = select(HabitModel).where(HabitModel.user_id == user.id)
        result: Result = await session.execute(stmt)
        habits = result.scalars().all()
        return list(habits)

    async def get_for_month(
        self,
        user: UserModel,
        month: int,
        year: int,
        session: AsyncSession,
    ) -> list[HabitModel] | None:

        _, last_day = calendar.monthrange(year, month)
        date = datetime.date(year, month, last_day)

        stmt = select(HabitModel).where(
            (HabitModel.user_id == user.id) & (HabitModel.created_at <= date)
        )
        result: Result = await session.execute(stmt)
        habits = result.scalars().all()
        return list(habits)


habit = HabitCRUD(HabitModel)
