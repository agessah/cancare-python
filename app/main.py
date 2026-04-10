from fastapi import FastAPI

from app.db import events  # noqa
from app.core.config import settings
from app.core.cors import setup_cors
from app.core.pagination import setup_pagination
from app.api.v1.router import api_router

def create_app() -> FastAPI:
    app = FastAPI(
        title="Cancer Care API", #settings.APP_NAME,
        debug=settings.DEBUG,
        version="1.0.0",
    )

    setup_cors(app)

    app.include_router(api_router, prefix="/api/v1")

    setup_pagination(app)

    return app

app = create_app()