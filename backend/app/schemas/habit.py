from pydantic import BaseModel, ConfigDict


class HabitBase(BaseModel):
    name: str
    goal: str
    user_id: str


class HabitUpdate(HabitBase):
    name: str | None = None
    goal: str | None = None
    user_id: str | None = None


class HabitCreate(HabitBase):
    pass


class HabitResponseModel(HabitBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
