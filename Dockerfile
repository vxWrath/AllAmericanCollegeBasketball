# ── Stage 1: build ────────────────────────────────────────────────────────────
# Install dependencies into an isolated venv so only the venv is copied to the
# runtime stage — no build tools, no pip cache, no compiler artifacts.
FROM python:3.14-slim AS builder

WORKDIR /build

RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# ── Stage 2: runtime ──────────────────────────────────────────────────────────
FROM python:3.14-slim AS runtime

# Non-root user for security
RUN addgroup --system app && adduser --system --ingroup app app

WORKDIR /app

# Copy venv from builder — no pip, no compiler
COPY --from=builder /venv /venv
ENV PATH="/venv/bin:$PATH"

# Copy application source
COPY migrations/ migrations/
COPY website/ website/
COPY alembic.ini .

USER app

# APP_PORT and LOG_LEVEL are injected at runtime via docker-compose environment.
# Shell form CMD is used so $APP_PORT and $LOG_LEVEL are expanded from the container env.
CMD uvicorn website.main:app --host 0.0.0.0 --port $APP_PORT --log-level $LOG_LEVEL
