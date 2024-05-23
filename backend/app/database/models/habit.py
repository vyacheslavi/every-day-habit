from pydantic import BaseModel
from sqlalchemy.orm import relationship, Mapped

from backend.app.database.base_model import Base
from backend.app.database.models.user import UserModel


class HabitModel(Base):

    __tablename__ = "habit"

    name: Mapped[str]
    goal: Mapped[int]
    user: Mapped["UserModel"] = relationship(back_populates="habits")
