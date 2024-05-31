from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app import crud
from backend.app.database.db_helper import db_helper
from backend.app.schemas import HabitResponseModel, HabitCreate, HabitUpdate
from backend.app.api import deps

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[deps.get_current_super_user],
)
