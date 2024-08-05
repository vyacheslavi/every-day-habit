from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get("/login/reminder", response_class=HTMLResponse)
async def register_template(
    request: Request,
):

    return templates.TemplateResponse(
        request=request, name="/auth/reminder/request-on-change.html"
    )


@router.get("/login/reminder/change-password", response_class=HTMLResponse)
async def verification_template(
    request: Request,
):
    return templates.TemplateResponse(
        request=request, name="/auth/reminder/change-password.html"
    )
