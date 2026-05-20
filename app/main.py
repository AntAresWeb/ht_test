from fastapi import FastAPI

from app.core.endpoints import router
from app.core.exceptions.handlers import registry
from app.core.settings import get_app_settings

app_settings = get_app_settings()
app = FastAPI(
    title=app_settings.app_title,
    description=app_settings.app_description,
)
app.include_router(router)
registry.register_all(app)
