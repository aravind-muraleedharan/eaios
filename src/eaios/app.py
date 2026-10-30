""" EAIOS Application entry point"""

import logging
import time
from collections.abc import Awaitable, Callable
from importlib.metadata import version

from fastapi import FastAPI, Request, Response

from eaios.core.config import get_settings
from eaios.core.logging_setup import setup_logging


settings = get_settings()
setup_logging(settings.log_level)
logger = logging.getLogger("eaios")
app_version = version("eaios")

# Hide the interactive API documentation in production

docs_enabled = settings.environment != "production"


app = FastAPI(
    title = settings.app_name,
    version = app_version,
    docs_url = "/docs" if docs_enabled else None,
    redoc_url = "/redoc" if docs_enabled else None,
)


logger.info(
    "application started",
    extra={"fields": {"environment": settings.environment, "version": app_version}},
)


@app.middleware("http")
async def log_requests(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    """Log the method, path, status and duration of every request."""
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = round((time.perf_counter() - start) * 1000, 2)

    logger.info(
        "request completed",
        extra={
            "fields": {
                "method": request.method,
                "path": request.url.path,
                "status": response.status_code,
                "duration_ms": duration_ms,
            }
        },
    )
    return response


@app.get("/health")
def health () -> dict[str, str]:
    "Report that the server is running"
    return {"status": "ok"}