from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app import crud, schemas
from backend.app.api import deps
from backend.app.database.db_helper import db_helper
from backend.app.database.models import UserModel


router = APIRouter(
    prefix="/notes",
    tags=["Notes"],
)


@router.get("/month/{month}/year/{year}/")
async def get_notes_for_month(
    month: int,
    year: int,
    user: UserModel = Depends(deps.get_current_active_verified_auth_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> list[schemas.NoteResponseModel] | None:
    return await crud.note.get_for_month(month, year, user, session)


@router.post("")
async def create_note(
    note: schemas.NoteCreate,
    user: UserModel = Depends(deps.get_current_active_verified_auth_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> bool:
    note = schemas.NoteInDb(**note.model_dump(), user_id=user.id)
    return await crud.note.create(note, session)


@router.patch(
    "/{note_id}",
    dependencies=[Depends(deps.get_current_active_verified_auth_user)],
)
async def update_habit_info(
    note_id: int,
    note: schemas.NoteUpdate,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.note.update(note_id, note, session)


@router.delete(
    "/{note_id}",
    dependencies=[Depends(deps.get_current_active_verified_auth_user)],
)
async def update_habit_info(
    note_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.note.delete(note_id, session)
