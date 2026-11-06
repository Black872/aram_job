# ARAM — AI Recruitment & Application Manager

Stage 1 foundation: FastAPI + PostgreSQL + SQLAlchemy + Alembic + Docker Compose.

## Requirements
- Docker Engine and Docker Compose plugin
- Git (recommended)
- An Ubuntu host or local Docker environment

## Quick start
1. Copy `.env.example` to `.env`.
2. Change `POSTGRES_PASSWORD` and `APP_SECRET_KEY`.
3. Start the stack:

   ```bash
   docker compose up --build -d
   ```

4. Check:
   - API health: http://localhost:8000/health
   - OpenAPI docs: http://localhost:8000/docs
   - PostgreSQL: localhost:5432 (only exposed to localhost)

5. Apply migrations:

   ```bash
   docker compose exec api alembic upgrade head
   ```

6. Run tests:

   ```bash
   docker compose exec api pytest
   ```

## Current scope
- Foundation only: application configuration, database connection, SQLAlchemy models,
  initial Alembic migration, health endpoint, and basic tests.
- No Gmail or Google Sheets credentials are required yet.
- No email polling or external writes happen in this stage.

## Data model
- `applications`: one row per job application.
- `email_events`: future Gmail messages; unique Gmail message ID prevents duplicates.
- `status_history`: immutable audit trail for status changes.
- `pending_actions`: proposed AI actions awaiting approval.
- `sync_state`: integration cursors and synchronization metadata.

The `applications` model includes fields corresponding to the current spreadsheet:
Company, Role Title, Salary/Rate, Link to Job Advert, Application Date,
Contact, Response, Interview Stage, Interview Time/Date & Interviewer Name,
Offer, plus internal normalized status and synchronization metadata.

Spreadsheet column mapping will be configured in Stage 2 after inspecting the actual
sheet headers and tab layout. The current sheet will not be modified in Stage 1.

## Security notes
- `.env` is excluded from Git.
- The database port is bound to `127.0.0.1` by default.
- Do not commit OAuth tokens, API keys, service-account JSON, or production data.
- Before exposing the API outside your LAN, add authentication and HTTPS/reverse proxy.
- Gmail integration will request read-only access and only process messages carrying
  the configured `Job Applications` label.

## Development commands
```bash
docker compose up --build -d
docker compose logs -f api
docker compose exec api alembic revision --autogenerate -m "describe change"
docker compose exec api alembic upgrade head
docker compose down
```

## Next stage
Stage 2 will inspect the existing Google Sheet's exact headers, import rows into
PostgreSQL, assign stable external row identifiers, and implement safe synchronization.
# aram_job
# aram_job
# aram_job
