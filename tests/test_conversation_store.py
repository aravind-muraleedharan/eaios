"""Tests for the in-memory conversation store.

Covers creating conversations, saving turns, trimming old turns, expiry (TTL),
the conversation limit, and that returned history is a safe copy.
"""

import pytest

from eaios.conversation_store.in_memory import InMemoryConversationStore


class FakeClock:
    """A clock we can move forward by hand, so tests don't sleep."""

    def __init__(self) -> None:
        self.now = 0.0

    def __call__(self) -> float:
        return self.now


@pytest.fixture
def clock() -> FakeClock:
    return FakeClock()


@pytest.fixture
def store(clock: FakeClock) -> InMemoryConversationStore:
    return InMemoryConversationStore(
        max_turns=2, ttl_seconds=60, max_conversations=3, clock=clock
    )


def test_new_conversation_starts_empty(store):
    conversation_id = store.new_conversation()
    assert store.get_history(conversation_id) == []


def test_append_turn_saves_question_and_answer(store):
    conversation_id = store.new_conversation()
    store.append_turn(conversation_id, "Hi", "Hello!")
    assert store.get_history(conversation_id) == [
        {"role": "user", "content": "Hi"},
        {"role": "assistant", "content": "Hello!"},
    ]


def test_unknown_id_returns_none(store):
    assert store.get_history("not-a-real-id") is None


def test_append_to_unknown_id_raises(store):
    with pytest.raises(KeyError):
        store.append_turn("not-a-real-id", "Hi", "Hello!")


def test_keeps_only_latest_turns(store):
    conversation_id = store.new_conversation()
    for n in range(3):
        store.append_turn(conversation_id, f"q{n}", f"a{n}")
    history = store.get_history(conversation_id)
    assert [m["content"] for m in history] == ["q1", "a1", "q2", "a2"]


def test_conversation_expires_after_ttl(store, clock):
    conversation_id = store.new_conversation()
    clock.now = 61
    assert store.get_history(conversation_id) is None


def test_using_a_conversation_keeps_it_alive(store, clock):
    conversation_id = store.new_conversation()
    clock.now = 50
    store.append_turn(conversation_id, "Hi", "Hello!")
    clock.now = 100  # 50 s since last use, still within 60
    assert store.get_history(conversation_id) is not None


def test_oldest_conversation_dropped_when_full(store):
    ids = [store.new_conversation() for _ in range(4)]  # limit is 3
    assert store.get_history(ids[0]) is None
    assert all(store.get_history(i) == [] for i in ids[1:])


def test_get_history_returns_a_copy(store):
    conversation_id = store.new_conversation()
    store.append_turn(conversation_id, "Hi", "Hello!")
    store.get_history(conversation_id).clear()
    assert len(store.get_history(conversation_id)) == 2
