# Local Dev Startup

## Prerequisites
- Docker Desktop running
- Python 3.14 installed

## First-time setup

**1. Clone and enter the repo**
```powershell
git clone <repo-url>
cd AllAmericanCollegeBasketball
```

**2. Create your dev env file**
```powershell
Copy-Item .env.example .env.dev
```
Open `.env.dev` and fill in values. The defaults in `.env.example` work for local dev — at minimum change the passwords.

**3. Install Python dependencies locally** (for editor tooling / running Alembic outside Docker)
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**4. Start the database and Redis**
```powershell
docker compose --env-file .env.dev up -d db redis
```

**5. Run migrations**
```powershell
docker compose --env-file .env.dev run --rm migrator
```

**6. Start the app**
```powershell
docker compose --env-file .env.dev up app
```

The app is now running at `http://localhost:<APP_PORT>`.

---

## Everyday commands

| Task | Command |
|---|---|
| Start everything | `docker compose --env-file .env.dev up` |
| Start in background | `docker compose --env-file .env.dev up -d` |
| Stop everything | `docker compose --env-file .env.dev down` |
| Wipe DB volume | `docker compose --env-file .env.dev down -v` |
| Run migrations | `docker compose --env-file .env.dev run --rm migrator` |
| View app logs | `docker compose --env-file .env.dev logs -f app` |
| Open psql | `docker compose --env-file .env.dev exec db psql -U <POSTGRES_USER> -d <POSTGRES_DB>` |

---

## Creating a new migration

After editing a model in `migrations/models/`:

```powershell
docker compose --env-file .env.dev run --rm migrator alembic revision --autogenerate -m "describe your change"
```

The volume mount writes the generated file directly to `migrations/versions/` on your host. Review it before applying — autogenerate is not perfect, always read the diff.

Apply it:
```powershell
docker compose --env-file .env.dev run --rm migrator
```

---

## Environment promotion

| Environment | Env file | How to deploy |
|---|---|---|
| dev | `.env.dev` | `docker compose --env-file .env.dev up` locally |
| QA | `.env.qa` | CI/CD on push to `qa` branch |
| prod | `.env.prod` | CI/CD on tagged release |

`.env.qa` and `.env.prod` are never committed — they live in GitHub Actions secrets and are written to the server at deploy time.
