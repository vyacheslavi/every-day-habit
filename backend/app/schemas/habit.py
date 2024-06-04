from datetime import date
from pydantic import BaseModel, ConfigDict


class HabitBase(BaseModel):
    name: str
    goal: int


class HabitUpdate(HabitBase):
    name: str | None = None
    goal: int | None = None


class HabitCreate(HabitBase):
    created_at: date


class HabitResponseModel(HabitBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class HabitInDb(HabitCreate):
    user_id: int
