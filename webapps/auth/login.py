from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.api import deps
from backend.app.database.db_helper import db_helper
from webapps.utils import get_user_via_request


templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get("/login", response_class=HTMLResponse)
async def login(
    request: Request,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    user = await get_user_via_request(request, session)
    if user:
        return RedirectResponse("/calendar")
    else:
        return templates.TemplateResponse("/auth/login.html", {"request": request})


@router.get("/logout")
async def logout(
    request: Request,
    response: Response,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    user = await get_user_via_request(request, session)
    response = RedirectResponse("/login")
    if user:
        response.delete_cookie("access_token")
    return response
