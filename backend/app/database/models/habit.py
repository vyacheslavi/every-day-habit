from datetime import date
import sys
from typing import TYPE_CHECKING
from sqlalchemy import Date, ForeignKey, func
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
