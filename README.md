
# Smart Incident Management System (SIMS)

A minimal, production-lean **incident monitoring and alerting** service built with **FastAPI**.  
It polls registered service health endpoints, detects incidents (downtime/slow responses), stores them, and fires alerts (Slack webhook).

> This is a starter you can push to GitHub immediately and extend with AI root-cause later.

## Features
- Register services with `name`, `url`, and `expected_status`.
- Background scheduler polls services every 30s (configurable).
- Detects incidents on HTTP error or latency threshold breach.
- Persists services and incidents in **SQLite** (simple to run anywhere).
- Alerts via **Slack Incoming Webhook** (optional).
- REST API to manage services and view incidents.

## Quickstart

### 1) Local (no Docker)
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r backend/requirements.txt
export SIMS_SLACK_WEBHOOK_URL=""  # optional
export SIMS_POLL_INTERVAL_SECONDS=30
uvicorn backend.app.main:app --reload
```

Open docs: http://127.0.0.1:8000/docs

### 2) Docker
```bash
docker compose up --build
```

### Environment Variables
- `SIMS_SLACK_WEBHOOK_URL` — Slack webhook to post alerts (optional).
- `SIMS_POLL_INTERVAL_SECONDS` — poll cadence (default 30).
- `SIMS_LATENCY_THRESHOLD_MS` — latency threshold in ms (default 1500).

### Example: register a service
```bash
curl -X POST http://127.0.0.1:8000/api/services   -H "Content-Type: application/json"   -d '{"name":"httpbin","url":"https://httpbin.org/status/200","expected_status":200}'
```

### Example: list incidents
```bash
curl http://127.0.0.1:8000/api/incidents
```

## Project Structure
```
smart-incident-mgr/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── settings.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── alerts.py
│   │   ├── monitor.py
│   │   └── routers/
│   │       ├── services.py
│   │       └── incidents.py
│   ├── requirements.txt
│   └── Dockerfile
└── docker-compose.yml
```

## Extend
- Add **AI root-cause suggestion** in `ai_responder.py` (stub provided) using OpenAI/HF.
- Switch to PostgreSQL by replacing `database.py` connection string and adding a Postgres service to `docker-compose.yml`.
- Add auth (JWT) and role-based access.
