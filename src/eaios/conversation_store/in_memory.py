"""Conversation store kept in server RAM: bounded, expiring, and lost on restart."""

import threading
import time
import uuid
from collections import OrderedDict
from collections.abc import Callable
from dataclasses import dataclass, field

from eaios.conversation_store.base import ChatMessage


@dataclass
class _Conversation:
    last_used: float
    messages: list[ChatMessage] = field(default_factory=list)


class InMemoryConversationStore:
    """Keeps each conversation's messages in RAM, keyed by conversation id."""

    def __init__(
        self,
        max_turns: int,
        ttl_seconds: float,
        max_conversations: int,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:

        self._max_messages = max_turns * 2  # one turn = question + answer
        self._ttl = ttl_seconds
        self._max_conversations = max_conversations
        self._clock = clock
        self._lock = threading.Lock()
        # Ordered from least to most recently used.
        self._conversations: OrderedDict[str, _Conversation] = OrderedDict()

    def new_conversation(self) -> str:
        conversation_id = str(uuid.uuid4())
        now = self._clock()
        with self._lock:
            self._remove_expired()
            if len(self._conversations) >= self._max_conversations:
                self._conversations.popitem(last=False)  # drop least recently used
            self._conversations[conversation_id] = _Conversation(last_used=now)
        return conversation_id

    def get_history(self, conversation_id: str) -> list[ChatMessage] | None:
        with self._lock:
            conversation = self._get_live(conversation_id)
            if conversation is None:
                return None
            return [ChatMessage(**m) for m in conversation.messages]  # a copy

    def append_turn(self, conversation_id: str, question: str, answer: str) -> None:
        with self._lock:
            conversation = self._get_live(conversation_id)
            if conversation is None:
                raise KeyError("conversation not found or expired")
            conversation.messages.append(ChatMessage(role="user", content=question))
            conversation.messages.append(ChatMessage(role="assistant", content=answer))
            del conversation.messages[: -self._max_messages]  # keep the latest turns
            conversation.last_used = self._clock()
            self._conversations.move_to_end(conversation_id)

    def _get_live(self, conversation_id: str) -> _Conversation | None:
        conversation = self._conversations.get(conversation_id)
        if conversation is None:
            return None
        if self._clock() - conversation.last_used > self._ttl:
            del self._conversations[conversation_id]
            return None
        return conversation

    def _remove_expired(self) -> None:
        now = self._clock()
        while self._conversations:
            oldest_id, oldest = next(iter(self._conversations.items()))
            if now - oldest.last_used <= self._ttl:
                break
            del self._conversations[oldest_id]
