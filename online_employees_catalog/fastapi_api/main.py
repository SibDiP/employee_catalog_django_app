from fastapi import FastAPI

from .config import settings
from .routers.employees import router as employees_router

app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description=settings.API_DESCRIPTION,
)


@app.get("/health", tags=["system"])
async def health() -> dict[str, str]:
    return {"status": "ok", "database": settings.DB_TYPE}


app.include_router(employees_router, prefix="/api")