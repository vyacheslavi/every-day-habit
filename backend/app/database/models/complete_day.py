from typing import TYPE_CHECKING
from pydantic import BaseModel
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.types import Date

from .base_model import Base

if TYPE_CHECKING:
    from backend.app.database.models.habit import HabitModel


class CompleteDayModel(Base):

    __tablename__ = "complete_day"

    habit_id: Mapped[int] = mapped_column(ForeignKey("habit.id"))
    date: Mapped[str] = mapped_column(Date)
    habit: Mapped["HabitModel"] = relationship()
