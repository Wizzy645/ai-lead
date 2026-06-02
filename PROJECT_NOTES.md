# Project Notes — Intelligent Lead Routing & Support API

## What this project is
This is an **AI-powered webhook processor** intended to route **sales leads** and **support inquiries**.

The repository currently contains:
- A **FastAPI** web endpoint that receives incoming webhook messages and returns a placeholder “decision”.
- A small **SQLAlchemy** data layer (async) to persist structured lead data (currently using **SQLite** locally).
- **Next-phase intent** captured in `TODO.md` and dependencies in `requirements.txt` (LangGraph/LangChain + Groq, with a plan toward Postgres + vector search).

## Current backend (Phase 1 / working implementation)

### API surface
- **Framework:** FastAPI
- **Endpoint:** `POST /api/v1/webhook/message`
- **Request model:** `WebhookPayload`
  - `customer_id: str`
  - `message: str`
- **Current behavior:** placeholder logic
  - Prints the message to stdout
  - Returns:
    - `status: "success"`
    - `decision: "pending_ai_classification"`
    - `original_message: payload.message`

> The LangGraph/LangChain agent routing/classification is expected to replace the placeholder in later phases.

### Data layer (SQLite async)
- **database.py**
  - Uses an **async SQLAlchemy engine**:
    - `DATABASE_URL = "sqlite+aiosqlite:///./agent_database.db"`
  - Exposes:
    - `AsyncSessionLocal`
    - `Base`
    - `get_db()` async generator

- **models.py**
  - Defines `SalesLead` table:
    - `sales_leads`
    - `id` (PK)
    - `customer_id`
    - `company_name` (nullable)
    - `budget` (nullable)
    - `original_message`
    - `created_at` (timezone-aware server default)

- **init_db.py**
  - Creates DB tables by running `Base.metadata.create_all`
  - Includes a Windows event-loop policy safeguard

## Intended direction (from TODO + dependencies)
The project is set up to eventually include:
- **AI classification / routing** using:
  - `langgraph`
  - `langchain`
  - `langchain-groq`
- **Vector / retrieval** support (planned)
  - `docker-compose.yml` provisions a Postgres + `pgvector` container (`pgvector/pgvector:pg17`)
- **Environment configuration**
  - `.env` is expected to hold Postgres and Groq placeholders (the file exists but is not readable from this tool environment)

## Docker / Postgres setup (planned infrastructure)
- **docker-compose.yml**
  - Service: `db` using `pgvector/pgvector:pg17`
  - Port mapping: `${POSTGRES_PORT}:5432`
  - Persistent volume: `postgres_data`

## How to run locally (based on current code)
1. Start with the SQLite DB initialization:
   - `python init_db.py`
   - This creates tables in `agent_database.db`.

2. Run the FastAPI server (using whatever command you typically use in this repo):
   - Server should expose `/docs` for Swagger UI.

## Notes / gaps to address next
- The webhook endpoint currently **does not**:
  - classify intent,
  - extract structured fields from `message`,
  - persist `SalesLead` records,
  - or use the LangGraph/LangChain agent pipeline yet.
- Integration points likely needed next:
  - load/initialize AI agent,
  - map AI output → `SalesLead` model fields,
  - write DB persistence logic,
  - switch/extend storage from SQLite to Postgres (pgvector) where appropriate.
