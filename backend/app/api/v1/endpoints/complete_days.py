from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app import crud
from backend.app.database.db_helper import db_helper
from backend.app.schemas import CompleteDay

router = APIRouter(
    prefix="/complete-days",
    tags=["Complete days"],
)


@router.get("/month/{month}/year/{year}/habit-id/{habit_id}")
async def get_days_from_the_month(
    month: int,
    year: int,
    habit_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> list[CompleteDay]:

    return await crud.complete_day.get_for_month(month, year, habit_id, session)


@router.post("/")
async def complete_day(
    complete_day: CompleteDay,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    await crud.complete_day.create(complete_day, session)


@router.delete("/")
async def delete_day(
    habit_id: CompleteDay,
    date: datetime,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    await crud.complete_day.delete(habit_id, date, session)
