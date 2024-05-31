from typing import TYPE_CHECKING

from pydantic import BaseModel
from sqlalchemy import ForeignKey, extract
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.types import Date
from sqlalchemy.ext.hybrid import hybrid_property

from .base_model import Base

if TYPE_CHECKING:
    from backend.app.database.models.habit import HabitModel


class CompleteDayModel(Base):

    __tablename__ = "complete_day"

    habit_id: Mapped[int] = mapped_column(ForeignKey("habit.id"))
    date: Mapped[str] = mapped_column(Date)
    habit: Mapped["HabitModel"] = relationship()

    @hybrid_property
    def date_year(self):
        return self.date.year

    @date_year.expression
    def date_year(cls):
        return extract("year", cls.date)

    @hybrid_property
    def date_month(self):
        return self.date.month

    @date_month.expression
    def date_month(cls):
        return extract("month", cls.date)

    @hybrid_property
    def date_day(self):
        return self.date.day

    @date_day.expression
    def date_day(cls):
        return extract("day", cls.date)
