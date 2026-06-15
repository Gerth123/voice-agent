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

