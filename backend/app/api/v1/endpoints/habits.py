from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app import crud
from backend.app.database.db_helper import db_helper
from backend.app.database.models.user import UserModel
from backend.app.schemas import HabitResponseModel, HabitCreate, HabitUpdate, HabitInDb
from backend.app.api import deps

router = APIRouter(
    prefix="/habits",
    tags=["Habits"],
)


@router.get("/", response_model=list[HabitResponseModel])
async def get_all_user_habits(
    user: UserModel = Depends(deps.get_current_active_verified_auth_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> list[HabitResponseModel] | None:
    habits = await crud.habit.get_all_from_user(user, session)
    return habits


@router.get("/month/{month}/year/{year}", response_model=list[HabitResponseModel])
async def get_user_habits_for_month(
    month: int,
    year: int,
    user: UserModel = Depends(deps.get_current_active_verified_auth_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> list[HabitResponseModel] | None:
    habits = await crud.habit.get_habits_for_month(user, month, year, session)
    return habits


@router.post("/")
async def create_new_habit(
    habit: HabitCreate,
    user: UserModel = Depends(deps.get_current_active_verified_auth_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> bool:
    user_id = user.id
    habit = HabitInDb(**habit.model_dump(), user_id=user_id)
    return await crud.habit.create(habit, session)


@router.delete(
    "/{habit_id}",
    dependencies=[Depends(deps.get_current_active_verified_auth_user)],
)
async def delete_habit(
    habit_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> bool:
    return await crud.habit.delete(habit_id, session)


@router.patch(
    "/{habit_id}",
    dependencies=[Depends(deps.get_current_active_verified_auth_user)],
)
async def update_habit_info(
    habit_id: int,
    habit: HabitUpdate,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> bool:
    return await crud.habit.update(habit_id, habit, session)
