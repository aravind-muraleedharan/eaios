"""Serve the chat window page and its static files."""

from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse

WEB_DIR = Path(__file__).parent
STATIC_DIR = WEB_DIR / "static"

router = APIRouter(include_in_schema=False)


@router.get("/")
def chat_page() -> FileResponse:
    """Return the chat window page."""
    return FileResponse(WEB_DIR / "index.html")
