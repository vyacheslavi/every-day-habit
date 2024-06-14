from fastapi import APIRouter

from .habits import router as habit_router
from .complete_days import router as cd_router
from .auth import router as auth_router
from .notes import router as notes_touter

router = APIRouter(prefix="/api/v1")

router.include_router(habit_router)
router.include_router(cd_router)
router.include_router(notes_touter)
router.include_router(auth_router)
