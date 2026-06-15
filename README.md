# Voice Agent

Production-oriented MVP for a personal AI voice agent.

## Structure

```text
voice-agent/
  backend/      FastAPI app, database models, provider adapters, privacy layer
  frontend/     Angular admin UI
  n8n/          Automation workflows
  docker-compose.yml
  .env.example
```

## MVP Focus

- Inbound calls first
- Clear AI disclosure at call start
- Short structured summaries: who, what, when, where
- Direct appointment booking for clear free slots
- iCal/CalDAV calendar integration first
- WhatsApp notifications via n8n
- Optional audio and transcript storage
- EU-hostable architecture

## Local Development

Backend:

```bash
cd backend
python -m venv .venv
.venv\Scripts\python -m pip install -e ".[dev]"
uvicorn app.main:app --reload
```

Database migrations:

```bash
cd backend
alembic upgrade head
```

Frontend:

```bash
cd frontend
npm install
npm start
```

Docker Compose:

```bash
docker compose up --build
```

On Windows, make sure Docker Desktop is running before starting Compose.

## API

FastAPI exposes OpenAPI docs at:

```text
http://localhost:8000/docs
```

Current MVP route groups:

- `/api/v1/health`
- `/api/v1/user-settings/me`
- `/api/v1/calls`
- `/api/v1/appointments`
- `/api/v1/calendar-connections`
- `/api/v1/ical-settings`
- `/api/v1/provider-settings/{voice|tts|stt|llm}`
- `/api/v1/webhooks/voice/*`
- `/api/v1/webhooks/n8n/*`

