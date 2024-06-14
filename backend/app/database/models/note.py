from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, extract
from sqlalchemy.types import Text, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property

from .base_model import Base

if TYPE_CHECKING:
    from backend.app.database.models import UserModel


class NoteModel(Base):

    __tablename__ = "note"

    text: Mapped[str] = mapped_column(Text)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    created_at: Mapped[str] = mapped_column(Date)
    user: Mapped["UserModel"] = relationship()

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
