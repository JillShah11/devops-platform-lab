import os

from fastapi import FastAPI

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