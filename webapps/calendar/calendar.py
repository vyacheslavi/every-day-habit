from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api import deps
from backend.app.database.db_helper import db_helper
from backend.app.database.models.user import UserModel
from webapps.utils import get_user_via_request

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get(
    "/calendar",
    response_class=HTMLResponse,
    # dependencies=[Depends(deps.get_current_active_verified_auth_user)],
)
async def get_caledar(
    request: Request, session: AsyncSession = Depends(db_helper.session_dependency)
):
    user = await get_user_via_request(request, session)
    if user:
        return templates.TemplateResponse(
            request=request,
            name="/calendar/calendar.html",
            context={"title": "Calendar", "user": user},
        )
    return RedirectResponse(
        url="/login",
        status_code=status.HTTP_308_PERMANENT_REDIRECT,
    )


@router.get("/", response_class=RedirectResponse)
async def get_main_page():
    return RedirectResponse(
        "/calendar",
        status_code=status.HTTP_308_PERMANENT_REDIRECT,
    )
