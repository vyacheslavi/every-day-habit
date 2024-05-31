from datetime import datetime
import sys
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .base_model import Base

if TYPE_CHECKING:
    from backend.app.database.models.user import UserModel


class HabitModel(Base):

    __tablename__ = "habit"

    name: Mapped[str]
    goal: Mapped[int]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=func.now(),
    )
    user: Mapped["UserModel"] = relationship(back_populates="habits")
