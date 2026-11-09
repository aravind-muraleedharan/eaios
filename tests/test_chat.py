"""Tests for the chat endpoint."""

import anthropic
import httpx

from eaios.api.chat import get_claude_client
from eaios.app import app


class FakeClaudeClient:
    """Stands in for ClaudeClient: records questions and returns a fixed answer."""

    def __init__(self) -> None:
        self.questions: list[str] = []

    async def ask(self, question: str) -> str:
        self.questions.append(question)
        return "This is a fake answer."


class FailingClaudeClient:
    """Stands in for ClaudeClient: always fails, like Claude being unreachable."""

    async def ask(self, question: str) -> str:
        raise anthropic.APIConnectionError(
            request=httpx.Request("POST", "https://api.anthropic.com")
        )


def test_chat_returns_answer(client):
    fake = FakeClaudeClient()
    app.dependency_overrides[get_claude_client] = lambda: fake

    response = client.post("/v1/chat", json={"question": "  What is RAG?  "})

    assert response.status_code == 200
    assert response.json()["answer"] == "This is a fake answer."
    assert "model" in response.json()
    assert fake.questions == ["What is RAG?"]  # whitespace was stripped


def test_chat_rejects_empty_question(client):
    fake = FakeClaudeClient()
    app.dependency_overrides[get_claude_client] = lambda: fake

    response = client.post("/v1/chat", json={"question": "   "})

    assert response.status_code == 422
    assert fake.questions == []  # Claude was never called


def test_chat_rejects_missing_question(client):
    response = client.post("/v1/chat", json={"text": "hello"})

    assert response.status_code == 422


def test_chat_returns_safe_error_when_claude_fails(client):
    app.dependency_overrides[get_claude_client] = lambda: FailingClaudeClient()

    response = client.post("/v1/chat", json={"question": "Hello"})

    assert response.status_code == 503
    assert response.json()["detail"] == (
        "The AI service is temporarily unavailable. Please try again."
    )
    assert "APIConnectionError" not in response.text  # no internal details leaked
