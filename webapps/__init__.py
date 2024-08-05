from fastapi import APIRouter

from .calendar import calendar
from .auth import router as auth_router


router = APIRouter()


router.include_router(calendar.router)
router.include_router(auth_router)
