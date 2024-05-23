from pydantic import BaseModel, EmailStr
from sqlalchemy import Boolean, LargeBinary
from sqlalchemy.orm import mapped_column, Mapped, relationship
from backend.app.database.base_model import Base
from backend.app.database.models.habit import HabitModel


class UserModel(Base):

    __tablename__ = "user"

    email: EmailStr = mapped_column(
        unique=True,
        index=True,
        nullable=False,
    )

    hashed_password: Mapped[str] = mapped_column(
        LargeBinary,
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    is_superuser: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    habits: Mapped[list["HabitModel"]] = relationship(
        back_populates="user",
    )
