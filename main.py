import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import api_router
from app.core.config import settings


def create_app() -> FastAPI:
    logging.info("Initialise fast-API app")
    _app = FastAPI()

    _app.include_router(api_router)

    # Set up CORS
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS_LIST,
        allow_credentials=True,
        allow_methods=settings.ALLOWED_REST_METHODS_LIST,
        allow_headers=["*"],
    )

    return _app


if __name__ == "__main__":

    try:
        app = create_app()
        uvicorn.run(app, host="0.0.0.0", port=8200, log_level="info")
    except Exception as e:
        logging.error(f"Error in fast-API app initialisation => {e}")
