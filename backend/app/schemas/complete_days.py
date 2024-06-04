from datetime import date
from pydantic import BaseModel


class CompleteDay(BaseModel):

    habit_id: int
    date: date
