# End-to-End AI Engineering Bootcamp

A sample end-to-end project demonstrating a lightweight AI application with a FastAPI backend and a Streamlit frontend. The project includes Docker compose for easy local development and deployment, example dataset files, and configuration for multiple LLM providers (OpenAI, Groq, Google GenAI).

**Status:** Prototype

**Contents**
- **apps/api** — FastAPI backend exposing a `/chat` endpoint.
- **apps/chatbot_ui** — Streamlit-based chat UI that consumes the API.
- **data/** — Example datasets and metadata files used for demos and notebooks.
- `docker-compose.yml`, `Makefile`, `env.example`, `pyproject.toml` — project-level tooling and configuration.

**Requirements**
- Python 3.12+
- Docker & Docker Compose (for containerized run)

Quick dependencies (see `pyproject.toml` for full list):
- `fastapi`, `uvicorn`, `streamlit`, `openai`, `google-genai`, `groq`, `pydantic`, `python-dotenv`

Getting started
---------------

1) Copy environment variables

Create a `.env` file in the repo root (or use environment variables) based on `env.example`:

```env
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
GROQ_API_KEY=your_groq_api_key_here
```

2) Run with Docker Compose (recommended)

Build and start both services (API + Streamlit UI):

```bash
docker-compose up --build
```

The services (per `docker-compose.yml`):
- Streamlit UI: http://localhost:8501
- API: http://localhost:8000

Alternate local development (without Docker)

- Create a virtual environment and install project deps. From repo root:

```bash
python -m venv .venv
source .venv/Scripts/activate   # Windows: .venv\Scripts\activate
pip install -e .[dev]
```

- Run the API (from `apps/api`):

```bash
uvicorn api.app:app --host 0.0.0.0 --port 8000 --reload
```

- Run the Streamlit UI (from `apps/chatbot_ui`):

```bash
streamlit run src/chatbot_ui/app.py
```

Project architecture
---------------------

- Backend (`apps/api`)
	- Exposes POST `/chat` which accepts JSON payload { `provider`, `model_name`, `messages` } and returns `{ "response": "..." }`.
	- Main LLM integration implemented in `apps/api/src/api/app.py` using provider-specific SDKs (OpenAI, Groq, Google GenAI).
	- Configuration loads API keys from `.env` via `pydantic-settings` (`apps/api/src/api/core/config.py`).

- Frontend (`apps/chatbot_ui`)
	- Streamlit app at `apps/chatbot_ui/src/chatbot_ui/app.py` with a simple chat UI.
	- Calls backend `/chat` endpoint using the configured `API_URL` from `apps/chatbot_ui/src/chatbot_ui/core/config.py`.

API usage example
------------------

Example request to the API `/chat` endpoint (JSON):

```json
POST /chat
Content-Type: application/json

{
	"provider": "OpenAI",
	"model_name": "gpt-5-mini",
	"messages": [
		{"role": "user", "content": "Say hello"}
	]
}
```

Example curl:

```bash
curl -X POST http://localhost:8000/chat \
	-H "Content-Type: application/json" \
	-d '{"provider":"OpenAI","model_name":"gpt-5-mini","messages":[{"role":"user","content":"Hello"}] }'
```

Notes & configuration
---------------------
- Environment: `env.example` includes `OPENAI_API_KEY`, `GOOGLE_API_KEY`, `GROQ_API_KEY`.
- Ports: Streamlit uses `8501`, API uses `8000` (as defined in `docker-compose.yml`).
- Python constraints: Project root `pyproject.toml` requests `requires-python = ">=3.12"`.

Development & testing
----------------------

- Use the included `Makefile` target `run-docker-compose` to run with Docker Compose.
- Unit tests and CI are not included in this prototype — consider adding tests for the API and UI interactions.

Contributing
------------

1. Create an issue describing the change.
2. Open a PR on a feature branch.

License
-------
This repository includes a `LICENSE` file at the project root.

Contact
-------
For questions contact the repository author listed in package metadata (e.g. `apps/api/pyproject.toml`).

----
Generated README based on project structure and source files.
