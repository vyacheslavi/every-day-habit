from datetime import date

from pydantic import BaseModel, ConfigDict


class NoteBase(BaseModel):
    text: str
    created_at: date


class NoteUpdate(BaseModel):
    text: str | None = None


class NoteCreate(NoteBase):
    pass


class NoteResponseModel(NoteBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class NoteInDb(NoteCreate):
    user_id: int
