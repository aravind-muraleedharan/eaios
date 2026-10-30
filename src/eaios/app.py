""" EAIOS Application entry point"""

from importlib.metadata import version

from fastapi import FastAPI

from eaios.core.config import get_settings


settings = get_settings()

# Hide the interactive API documentation in production

docs_enabled = settings.environment != "production"


app = FastAPI(
    title = settings.app_name,
    version = version("eaios"),
    docs_url = "/docs" if docs_enabled else None,
    redoc_url = "/redoc" if docs_enabled else None,
)


@app.get("/health")
def health () -> dict[str, str]:
    "Report that the server is running"
    return {"status": "ok"}