import sys
from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, extract
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, Mapped, mapped_column


from .base_model import Base

if TYPE_CHECKING:
    from backend.app.database.models.user import UserModel


class HabitModel(Base):

    __tablename__ = "habit"

    name: Mapped[str]
    goal: Mapped[int]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    created_at: Mapped[str] = mapped_column(Date)
    user: Mapped["UserModel"] = relationship(back_populates="habits")

    @hybrid_property
    def created_at_year(self):
        return self.created_at.year

    @created_at_year.expression
    def created_at_year(cls):
        return extract("year", cls.created_at)

    @hybrid_property
    def created_at_month(self):
        return self.created_at.month

    @created_at_month.expression
    def created_at_month(cls):
        return extract("month", cls.created_at)
