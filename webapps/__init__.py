from fastapi import APIRouter

from .calendar import calendar
from .auth import login, register


router = APIRouter()


router.include_router(calendar.router)
router.include_router(login.router)
router.include_router(register.router)
