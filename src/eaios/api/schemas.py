"""Request and response models for the HTTP API."""

from pydantic import BaseModel, ConfigDict, Field

from eaios.core.config import get_settings

settings = get_settings()


class ChatRequest(BaseModel):
    """A question sent to the chat endpoint."""

    model_config = ConfigDict(str_strip_whitespace = True)

    question: str = Field(min_length = 1, max_length = settings.chat_max_ques_chars)


class ChatResponse(BaseModel):
    """The answer returned by the chat endpoint."""

    answer: str
    model: str



