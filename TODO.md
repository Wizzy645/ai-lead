# Project Setup - Phase 1 (Infrastructure & Environment Setup)

## Step 1: Create environment variables file
- [x] Create `.env` in repo root with Postgres + Groq placeholders

## Step 2: Define database container
- [x] Create `docker-compose.yml` using `pgvector/pgvector:pg17`

## Step 3: Install backend dependencies
- [x] Create `requirements.txt` with FastAPI/Uvicorn/Pydantic + LangGraph + Groq + pgvector stack

## Step 4: Build FastAPI entry point
- [x] Create `main.py` with webhook endpoint `/api/v1/webhook/message`

## Step 5: Run & verify
- [x] Create venv + `pip install -r requirements.txt`
- [x] `python init_db.py` (creates `agent_database.db`)
- [x] Verify API wiring by importing app + exercising endpoint via TestClient
- [x] Verify `http://localhost:8000/docs` is available when running server locally

# Phase 2: Building the Data Layer (SQLAlchemy)

## Step 1: Create database.py
- [x] `database.py` (SQLite async engine + session factory + Base)

## Step 2: Create models.py
- [x] `models.py` (SalesLead only; pgvector SupportDocument removed)

## Step 3: Create init_db.py
- [x] `init_db.py` (creates tables for SQLite)

## Step 4: Initialize DB
- [x] Run `python init_db.py`
