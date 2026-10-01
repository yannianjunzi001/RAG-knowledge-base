from alembic.context import configure
from fastapi import FastAPI
import fastapi
from fastapi.middleware.cors import CORSMiddleware

from app.api.error_handlers import register_error_handlers
from app.core.config import settings
from app.core.logging import configure_logging, get_logger
from app.api.routes import documents,health,chat

def create_app() ->FastAPI:
    configure_logging()
    logger= get_logger(__name__)

    app=FastAPI(title=settings.app_name)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_error_handlers(app)
    app.include_router(health.router, prefix="/api")

    app.include_router(documents.router, prefix="/api")

    app.include_router(chat.router, prefix="/api")

    logger.info("app initialized: %s",settings.app_name)
    return app

app=create_app()