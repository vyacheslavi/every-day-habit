from pydantic import BaseModel


class CompleteDay(BaseModel):

    habit_id: int
    date: str
