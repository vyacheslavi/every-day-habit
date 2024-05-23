from pydantic import BaseModel
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.types import Date

from backend.app.database.base_model import Base
from backend.app.database.models.habit import HabitModel


class CompleteDayModel(Base):

    __tablename__ = "complete_day"

    habit_id: Mapped[int] = mapped_column(ForeignKey("Habbit.id"))
    date: Date = mapped_column()
    habit: Mapped["HabitModel"] = relationship()
