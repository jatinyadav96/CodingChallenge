from fastapi import APIRouter

from app.core.config import settings
from app.routes import routes_drawing

api_router = APIRouter()

base_prefix = settings.API_VERSION_PREFIX

api_router.include_router(
    routes_drawing.router,
    prefix=f"{base_prefix}/drawings",
    tags=["Drawings"],
)
