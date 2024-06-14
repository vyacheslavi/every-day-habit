from typing import TYPE_CHECKING

from pydantic import EmailStr
from sqlalchemy import Boolean, LargeBinary
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .base_model import Base

if TYPE_CHECKING:
    from backend.app.database.models.habit import HabitModel


class UserModel(Base):

    __tablename__ = "user"

    email: Mapped[str] = mapped_column(
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
    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    habits: Mapped[list["HabitModel"]] = relationship(
        back_populates="user",
        cascade="all, delete",
    )
