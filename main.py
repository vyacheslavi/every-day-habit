import sys
from pathlib import Path

from fastapi import FastAPI
import fastapi
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from fastapi.openapi.docs import (
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
import uvicorn

from backend.app.api import api_v1_router
from backend.app.core.config import settings
from webapps import router as webapps_router


def initialize_backend_application() -> fastapi.FastAPI:

    templates = Jinja2Templates(directory="templates")

    main_app = FastAPI(docs_url=None, redoc_url=None)

    main_app.mount("/static", StaticFiles(directory="static"), name="static")

    @main_app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=main_app.openapi_url,
            title=main_app.title + " - Swagger UI",
            oauth2_redirect_url=main_app.swagger_ui_oauth2_redirect_url,
            swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
            swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
        )

    @main_app.get(main_app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
    async def swagger_ui_redirect():
        return get_swagger_ui_oauth2_redirect_html()

    main_app.include_router(api_v1_router)
    main_app.include_router(webapps_router)

    return main_app


backend_app: fastapi.FastAPI = initialize_backend_application()


if __name__ == "__main__":
    uvicorn.run(
        "main:backend_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
        forwarded_allow_ips="*",
    )
