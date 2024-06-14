from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.database.db_helper import db_helper
from webapps import utils

templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get("/register", response_class=HTMLResponse)
async def register_template(
    request: Request, session: AsyncSession = Depends(db_helper.session_dependency)
):
    user = await utils.get_user_via_request(request, session)
    if not user:
        return templates.TemplateResponse(request=request, name="/auth/register.html")
    else:
        return RedirectResponse("/calendar")


@router.get("/verificator", response_class=HTMLResponse)
async def verification_template(
    request: Request,
):
    return templates.TemplateResponse(request=request, name="/auth/verification.html")
