from datetime import datetime
from pydantic import BaseModel, ConfigDict


class HabitBase(BaseModel):
    name: str
    goal: int


class HabitUpdate(HabitBase):
    name: str | None = None
    goal: int | None = None


class HabitCreate(HabitBase):
    pass


class HabitResponseModel(HabitBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


class HabitInDb(HabitBase):
    user_id: int
