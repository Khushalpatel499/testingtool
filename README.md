# 🛠️ DevTool — API Tester + Webhook Inspector

A production-quality developer tool combining **Postman-like API testing** with **Webhook.site-style webhook inspection**, built with **Streamlit** (frontend) and **FastAPI** (backend).

## Architecture

```
Clean Architecture with Loose Coupling
├── Frontend (Streamlit) — UI only, no business logic
├── Backend (FastAPI) — Business logic, HTTP engine, webhook receiver
├── Shared — Contracts and constants
└── In-Memory Storage — No database required
```

**Key Principles:**
- Service-layer pattern
- Separation of concerns (UI / Logic / Transport / Storage)
- Independent modules (API Tester ≠ Webhook Tester)
- Webhook receiver works independently from Streamlit UI

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the backend

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Start the frontend

```bash
streamlit run frontend/app.py
```

Open http://localhost:8501 in your browser.

## Module 1: API Tester

- Send GET, POST, PUT, PATCH, DELETE requests
- Set headers, query params, body, auth
- Bearer Token, Basic Auth, API Key support
- cURL import
- JSON validation
- Response viewer with status, timing, headers, body
- Session request history

## Module 2: Webhook Tester

- Generate unique webhook URLs
- Accept ANY HTTP method and content type
- Inspect captured requests: headers, body, query params, IP
- Auto-refresh event viewer
- Works with any language/platform (curl, Python, JS, Java, Go, etc.)

### Example: Send a webhook

```bash
curl -X POST http://localhost:8000/hook/YOUR_ENDPOINT_ID \
  -H "Content-Type: application/json" \
  -d '{"event": "user.created", "data": {"id": 123}}'
```

## Project Structure

```
├── frontend/          # Streamlit UI
│   ├── app.py         # Entry point
│   ├── pages/         # Page modules
│   ├── components/    # Reusable UI components
│   ├── services/      # Backend communication layer
│   └── utils/         # UI helpers
├── backend/           # FastAPI backend
│   ├── main.py        # Entry point
│   ├── routes/        # API route handlers
│   ├── services/      # Business logic
│   ├── storage/       # In-memory stores
│   ├── models/        # Pydantic models
│   ├── parsers/       # Content-type parsers
│   └── utils/         # Helpers
├── shared/            # Shared schemas and constants
├── requirements.txt
└── README.md
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/send` | POST | Execute an API test request |
| `/api/history` | GET | Get request history |
| `/api/history` | DELETE | Clear history |
| `/webhooks/create` | POST | Create webhook endpoint |
| `/webhooks/list` | GET | List all endpoints |
| `/webhooks/{id}/events` | GET | Get captured events |
| `/webhooks/{id}/events` | DELETE | Clear events |
| `/webhooks/{id}` | DELETE | Delete endpoint |
| `/hook/{id}` | ANY | Webhook receiver |
| `/health` | GET | Health check |
