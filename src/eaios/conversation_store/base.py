"""
Defines the message structure and the methods every conversation store must have.
"""

from typing import Literal, Protocol, TypedDict


class ChatMessage(TypedDict):
    """One message, in the shape the Claude API expects."""

    role: Literal["user", "assistant"]
    content: str


class ConversationStore(Protocol):
    """What any conversation store must do. A database one can replace RAM later."""

    def new_conversation(self) -> str: ...

    def get_history(self, conversation_id: str) -> list[ChatMessage] | None: ...

    def append_turn(self, conversation_id: str, question: str, answer: str) -> None: ...
