from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app import crud
from backend.app.database.db_helper import db_helper
from backend.app.database.models.user import UserModel
from backend.app import schemas
from backend.app.api import deps, exceptions

router = APIRouter(
    prefix="/habits",
    tags=["Habits"],
)


@router.get("/", response_model=list[schemas.HabitResponseModel])
async def get_all_user_habits(
    user: UserModel = Depends(deps.get_current_active_verified_auth_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> list[schemas.HabitResponseModel] | None:
    habits = await crud.habit.get_all_from_user(user, session)
    return habits


@router.get(
    "/month/{month}/year/{year}", response_model=list[schemas.HabitResponseModel]
)
async def get_user_habits_for_month(
    month: int,
    year: int,
    user: UserModel = Depends(deps.get_current_active_verified_auth_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> list[schemas.HabitResponseModel] | None:
    habits = await crud.habit.get_for_month(user, month, year, session)
    return habits


@router.post("/")
async def create_new_habit(
    habit: schemas.HabitCreate,
    user: UserModel = Depends(deps.get_current_active_verified_auth_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> bool:
    if habit.goal > 30:
        raise exceptions.too_large_goal
    habit = schemas.HabitInDb(**habit.model_dump(), user_id=user.id)
    return await crud.habit.create(habit, session)


@router.delete(
    "/{habit_id}",
    dependencies=[Depends(deps.get_current_active_verified_auth_user)],
)
async def delete_habit(
    habit_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.habit.delete(habit_id, session)


@router.patch(
    "/{habit_id}",
    dependencies=[Depends(deps.get_current_active_verified_auth_user)],
)
async def update_habit_info(
    habit_id: int,
    habit: schemas.HabitUpdate,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> bool:
    if habit.goal > 30:
        raise exceptions.too_large_goal
    return await crud.habit.update(habit_id, habit, session)
