"""Chat endpoint: send a question to Claude and return the answer."""

import logging
from functools import lru_cache
from typing import Annotated

import anthropic
from fastapi import APIRouter, Depends, HTTPException, status

from eaios.api.schemas import ChatRequest, ChatResponse
from eaios.core.config import get_settings
from eaios.llm.claude_client import ClaudeClient

logger = logging.getLogger("eaios")
router = APIRouter(prefix="/v1", tags=["chat"])


@lru_cache
def get_claude_client() -> ClaudeClient:
    """Create the Claude client once and reuse it for every request."""
    return ClaudeClient(get_settings())


@router.post("/chat")
async def chat(
    chat_request: ChatRequest,
    client: Annotated[ClaudeClient, Depends(get_claude_client)],
) -> ChatResponse:
    """Answer one question using Claude."""
    settings = get_settings()

    try:
        answer = await client.ask(chat_request.question)
    except anthropic.APIError:
        logger.exception("claude request failed")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The AI service is temporarily unavailable. Please try again.",
        ) from None

    log_fields = {
        "model": settings.claude_model,
        "question_chars": len(chat_request.question),
        "answer_chars": len(answer),
    }
    if settings.log_chat_content:
        log_fields["question"] = chat_request.question
        log_fields["answer"] = answer
    logger.info("chat completed", extra={"fields": log_fields})

    return ChatResponse(answer=answer, model=settings.claude_model)