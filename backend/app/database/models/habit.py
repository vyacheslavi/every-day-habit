import sys
from typing import TYPE_CHECKING
from sqlalchemy.orm import relationship, Mapped

from .base_model import Base

if TYPE_CHECKING:
    from backend.app.database.models.user import UserModel


class HabitModel(Base):

    __tablename__ = "habit"

    name: Mapped[str]
    goal: Mapped[int]
    user: Mapped["UserModel"] = relationship(back_populates="habits")
