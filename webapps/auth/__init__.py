from fastapi import APIRouter

from .register import router as register_router
from .login import router as login_router
from .reminder import router as reminder_router

router = APIRouter()

router.include_router(register_router)
router.include_router(login_router)
router.include_router(reminder_router)
