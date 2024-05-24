from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
import uvicorn

from backend.app.api.api_v1 import router as api_v1_router
from backend.app.core.config import settings

main_app = FastAPI(
    responses=ORJSONResponse,
)


@main_app.get("/")
async def root():
    return {"message": "Hello World"}


main_app.include_router(api_v1_router)


if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
