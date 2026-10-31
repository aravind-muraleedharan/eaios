"""Client for communicating with Claude."""

import anthropic

from eaios.core.config import Settings

class ClaudeClient:
    """Send questions to Claude and return its answers."""

    def __init__(self, settings: Settings) -> None:
        self._client = anthropic.AsyncAnthropic(
            api_key = settings.anthropic_api_key.get_secret_value(),
            timeout = settings.claude_timeout_sec,
            max_retries=2,
        )

        self._model = settings.claude_model
        self._max_tokens = settings.claude_max_tokens
        self._claude_sys_prompt = settings.system_prompt_file.read_text(encoding = "utf-8").strip()

    async def ask(self, question: str) -> str:
        """Send one question to claude and return the answer"""
        response = await self._client.messages.create(
            model = self._model,
            max_tokens = self._max_tokens,
            system = self._claude_sys_prompt,
            messages = [{"role": "user", "content": question}],
        )

        return "".join(
            block.text for block in response.content if block.type == "text"
        )
