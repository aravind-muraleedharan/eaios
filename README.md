# Enterprise Artificial Intelligence Operating System (EAIOS)

[![CI](https://github.com/aravind-muraleedharan/eaios/actions/workflows/ci.yml/badge.svg)](https://github.com/aravind-muraleedharan/eaios/actions/workflows/ci.yml)

EAIOS is an integrated platform for building, running, and governing AI systems across an enterprise. It brings the core building blocks of enterprise AI together under one roof, so teams can develop AI applications faster while keeping governance consistent and planned.

> **Status:** early development, built in public with one commit a day. APIs may change.

## What works today

- **Chat app:** a browser chat window backed by Claude
- **Versioned API:** `POST /v1/chat` with request validation and safe error handling
- **Configuration:** typed settings from environment variables; the app refuses to start on invalid values
- **Configurable system prompt:** kept in `prompts/system.md`, outside the code
- **Structured logging:** JSON logs to the console and a rotating file, with chat content logging off by default
- **Quality checks:** tests, linting, formatting, and security checks run on every push

## Architecture

```
Browser chat window
      │  POST /v1/chat
      ▼
EAIOS API (FastAPI)
  ├─ request logging (middleware)
  ├─ input validation (Pydantic)
  └─ chat endpoint
      │
      ▼
Claude client ──► Anthropic API
```

The browser never talks to Claude directly, so the API key stays on the server.

## Security and responsible AI choices

- Secrets come only from the environment and are hidden when settings are printed or logged
- Every request is validated before it reaches the model; oversized or empty input is rejected
- Users see generic error messages; technical details go only to server logs
- Model output is displayed as plain text, preventing cross-site scripting (XSS)
- Logging of chat content is opt-in, for privacy
- API documentation pages are disabled in production
- CI actions are pinned to exact commits, and run with read-only permissions

## Getting started

**Requirements:** [uv](https://docs.astral.sh/uv/) and an [Anthropic API key](https://console.anthropic.com/). uv installs the right Python version automatically.

```bash
git clone https://github.com/aravind-muraleedharan/eaios.git
cd eaios
uv sync
cp .env.example .env
```

Edit `.env` and set your key:

```
EAIOS_ANTHROPIC_API_KEY=your-api-key-here
```

Start the server:

```bash
uv run fastapi dev src/eaios/app.py
```

Then open:

- `http://127.0.0.1:8000/`: the chat window
- `http://127.0.0.1:8000/docs`: interactive API documentation

See `.env.example` for all available settings.

## Development

```bash
uv run pytest              # run the tests
uv run ruff check .        # lint (bugs, style, security)
uv run ruff format .       # format the code
```

## Roadmap

- [x] Secure chat app with Claude
- [ ] Conversation history
- [ ] Audit log
- [ ] Guardrails: prompt injection, personal data, output checks
- [ ] Policy engine (rules as configuration)
- [ ] Users, login, and roles
- [ ] Retrieval-augmented generation (RAG)
- [ ] Agentic AI

## License

Licensed under the MIT License. See [LICENSE](LICENSE) for details.