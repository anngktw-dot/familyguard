# FamilyGuard

A consent-first **family safety / parental-control MVP** with a FastAPI backend, persistent local storage, and separate parent/child web experiences.

> **Portfolio status:** this repository is a cleaned-up reconstruction of an earlier personal project concept. It demonstrates the product flow and backend architecture without pretending to be production monitoring software.

## Product idea

FamilyGuard is built around transparent family safety rather than hidden surveillance. A child intentionally shares a check-in; the parent dashboard can then display the latest shared status and a small set of device-usage summaries.

### Parent experience

- view the child's latest check-in;
- see an intentionally shared location label;
- see battery level and last check-in time;
- view screen-time and top-app summaries;
- refresh the dashboard from the API.

### Child experience

- choose a status message;
- choose what location label to share;
- share battery level;
- send the check-in explicitly.

## Tech stack

**Backend:** Python · FastAPI · Pydantic · SQLAlchemy · SQLite  
**Frontend:** HTML · CSS · JavaScript  
**Quality:** Pytest · Ruff · GitHub Actions · Docker

## Architecture

```text
familyguard/
├── backend/
│   ├── main.py          # FastAPI routes and app lifecycle
│   ├── db.py            # SQLAlchemy engine/session
│   ├── models.py        # persistent database models
│   ├── schemas.py       # request/response validation
│   └── tests/           # API tests
├── web/
│   ├── index.html       # parent dashboard
│   ├── child.html       # child check-in screen
│   ├── app.js
│   └── styles.css
├── .github/workflows/ci.yml
├── Dockerfile
└── pyproject.toml
```

## Run locally

### 1. Start the API

From the repository root:

```bash
python -m venv .venv
```

Activate it:

```bash
# macOS / Linux
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Install dependencies and start the server:

```bash
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload
```

API: `http://127.0.0.1:8000`  
Swagger docs: `http://127.0.0.1:8000/docs`

### 2. Start the web demo

In another terminal:

```bash
cd web
python -m http.server 5173
```

Open:

- Parent dashboard: `http://127.0.0.1:5173/index.html`
- Child check-in: `http://127.0.0.1:5173/child.html`

## API

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/health` | Health check |
| `GET` | `/children` | List children |
| `GET` | `/children/{id}` | Read current shared state |
| `POST` | `/children/{id}/check-in` | Submit an explicit check-in |
| `POST` | `/children/{id}/usage` | Update usage summary |

## Tests and linting

```bash
pip install -r backend/requirements-dev.txt
ruff check backend
pytest -q
```

The same checks run automatically in GitHub Actions.

## Docker

```bash
docker build -t familyguard .
docker run --rm -p 8000:8000 familyguard
```

## Privacy & safety boundary

This demo intentionally does **not** implement covert screenshots, message interception, microphone capture, hidden browser-history collection, or silent precise-location tracking. Shared information is explicit and visible in the product flow.

## Next product steps

- parent/child authentication and family invitations;
- PostgreSQL for hosted deployments;
- role-based authorization;
- encrypted device-to-account pairing;
- notification preferences;
- audit history for shared check-ins.
