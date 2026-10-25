import os

import psycopg
from fastapi import FastAPI, HTTPException

app = FastAPI(title="devops-platform-lab")

# Injected at deploy time so we can see which build is running
VERSION = os.getenv("APP_VERSION", "dev")


@app.get("/")
def root():
    return {"message": "Hello from devops-platform-lab", "version": VERSION}


@app.get("/healthz")
def healthz():
    # Kubernetes liveness/readiness probes will call this
    return {"status": "ok"}

@app.get("/db")
def db_check():
    # Credentials come from env vars injected by Kubernetes from the db-credentials Secret
    try:
        with psycopg.connect(
            host=os.getenv("DB_HOST", "localhost"),
            dbname=os.getenv("DB_NAME", "app"),
            user=os.getenv("DB_USER", "app"),
            password=os.getenv("DB_PASSWORD", ""),
            connect_timeout=3,
        ) as conn:
            version = conn.execute("SELECT version()").fetchone()[0]
        return {"database": "connected", "version": version}
    except psycopg.OperationalError as exc:
        # Don't leak connection details to the caller
        raise HTTPException(status_code=503, detail="database unavailable") from exc