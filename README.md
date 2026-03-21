# Session Management & Metrics API

A production-ready FastAPI service backed by SQLite that supports real session lifecycle management (start/stop), background data generation, and database-backed metrics retrieval.

## Architecture

```
API_Task/
├── main.py                    ← App entry point
├── requirements.txt           ← Python dependencies
├── README.md                  ← This file
├── .gitignore
├── database/
│   └── sessions.db            ← SQLite database (auto-created)
└── src/
    └── api/
        ├── __init__.py
        ├── models.py          ← SQLAlchemy ORM models (5 tables)
        ├── db.py              ← Engine, SessionLocal, init_db, seed_data
        ├── schemas.py         ← Pydantic response/request schemas
        ├── service.py         ← Background worker + metrics computation
        └── routes.py          ← All API endpoints
```

## Database Schema

| Table | Description | Foreign Key |
|-------|-------------|-------------|
| `sessions` | Parent — id, title, start_time, end_time, instructor_name, status | — |
| `attendance_metrics` | Attendance count + engagement score per tick | → sessions.id |
| `transcripts` | Speaker, text, is_question per tick | → sessions.id |
| `speech_metrics` | WPM, silence_gap, tone_variance per tick | → sessions.id |
| `session_reports` | Summary, key_topics, overall_score (generated on stop) | → sessions.id |

## Setup & Run

### 1. Create virtual environment & install dependencies

```bash
cd c:\Users\ashra\Desktop\API_Task
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Start the server

```bash
uvicorn main:app --reload --port 8000
```

**Expected output:**
```
2026-03-21 18:10:00 | INFO    | api.main        | APPLICATION STARTUP
2026-03-21 18:10:00 | INFO    | api.db          | Database initialized — all tables created
2026-03-21 18:10:00 | INFO    | api.db          | Seed data inserted — session id=1 created
2026-03-21 18:10:00 | INFO    | api.main        | Startup complete — API is ready
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### 3. Open API docs

Visit [http://localhost:8000/docs](http://localhost:8000/docs) to see the interactive Swagger UI.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/api/sessions` | List all sessions |
| GET | `/api/sessions/active` | Get active sessions |
| GET | `/api/sessions/{id}` | Get session by ID |
| POST | `/api/sessions/{id}/start` | Start session + background worker |
| POST | `/api/sessions/{id}/stop` | Stop session + generate report |
| GET | `/api/sessions/{id}/metrics` | Aggregated metrics (computed from DB) |
| GET | `/api/sessions/{id}/attendance` | Attendance timeline |
| GET | `/api/sessions/{id}/engagement` | Engagement scores over time |
| GET | `/api/sessions/{id}/transcript` | Full transcript |
| GET | `/api/sessions/{id}/report` | Session report |
| GET | `/api/sessions/{id}/scores` | Computed scores only |

## Testing with curl

```bash
# 1. List sessions (should show seeded session id=1)
curl http://localhost:8000/api/sessions

# 2. Start session 1 — triggers real background data generation
curl -X POST http://localhost:8000/api/sessions/1/start

# 3. Wait 10-15 seconds for data to accumulate...

# 4. Get real metrics computed from DB
curl http://localhost:8000/api/sessions/1/metrics

# 5. Get transcript entries
curl http://localhost:8000/api/sessions/1/transcript

# 6. Get attendance timeline
curl http://localhost:8000/api/sessions/1/attendance

# 7. Get engagement over time
curl http://localhost:8000/api/sessions/1/engagement

# 8. Try duplicate start — should return 400 error
curl -X POST http://localhost:8000/api/sessions/1/start

# 9. Stop session — generates final report
curl -X POST http://localhost:8000/api/sessions/1/stop

# 10. Get the generated report
curl http://localhost:8000/api/sessions/1/report

# 11. Get scores
curl http://localhost:8000/api/sessions/1/scores

# 12. Test error handling — non-existent session
curl http://localhost:8000/api/sessions/999/metrics
```

## How /start Triggers Real Processing

When `POST /api/sessions/{id}/start` is called:

1. The session status is set to `"active"` and `start_time` is recorded
2. An `asyncio.Task` is created via `SessionWorker` that runs a continuous loop
3. **Every ~3 seconds**, the loop inserts real rows into:
   - `attendance_metrics` — attendance count and engagement score
   - `transcripts` — speaker dialogue with question detection
   - `speech_metrics` — words-per-minute, silence gaps, tone variance
4. Data uses realistic values from curated pools (ML lecture content)
5. The worker is tracked in a task registry — **calling /start twice returns 400**

## How /metrics Reads from SQLite

When `GET /api/sessions/{id}/metrics` is called:

1. Queries `attendance_metrics` for avg engagement, peak/final attendance, dropoff rate
2. Queries `speech_metrics` for avg WPM and silence ratio
3. Queries `transcripts` for question/interaction ratio
4. **Computes derived scores** (engagement, clarity, interaction, overall) — each 0-100
5. Returns the complete `MetricsResponse` — **nothing is hardcoded**

## Error Handling

- All endpoints return consistent `{"status": "...", "message": "...", "data": ...}` envelope
- Invalid session IDs → 404 with JSON error
- Duplicate start → 400 with explanation
- Stop on inactive session → 400 with explanation
- Validation errors → 422 with details

## Logging

Every API request, session start/stop, background worker event, and DB operation is logged with structured format:
```
2026-03-21 18:12:00 | INFO    | api.routes      | POST /api/sessions/1/start
2026-03-21 18:12:00 | INFO    | api.service     | Background worker STARTED for session 1
```

## Suggested Git Workflow

```bash
cd c:\Users\ashra\Desktop\API_Task
git init
git add .
git commit -m "feat: implement session management API with real-time background data generation

- SQLAlchemy ORM with 5 tables (sessions, attendance, transcripts, speech, reports)
- 11 REST endpoints with consistent JSON response envelope
- Background asyncio worker generates realistic data every 3 seconds
- Computed metrics from actual DB rows (not hardcoded)
- Session lifecycle: idle → active → completed
- Auto-generated reports on session stop
- Structured logging throughout
- Pydantic v2 schemas for all responses"

git remote add origin <YOUR_GITHUB_REPO_URL>
git branch -M main
git push -u origin main
```
