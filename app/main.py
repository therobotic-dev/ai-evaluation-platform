
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.api.routes.evaluations import router as evaluations_router
from app.api.routes.rubrics import router as rubrics_router
from app.api.routes.analytics import router as analytics_router
from app.api.routes.disagreements import router as disagreements_router
from app.api.routes.audit import router as audit_router


app = FastAPI(
    title="AI Evaluation Platform",
    description="A platform for managing AI evaluation and quality assessment.",
    version="0.1.0",
)


app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static",
)


app.include_router(
    evaluations_router,
    prefix="/evaluations",
    tags=["Evaluations"],
)

app.include_router(
    rubrics_router,
    prefix="/rubrics",
    tags=["Rubrics"],
)

app.include_router(
    analytics_router,
    prefix="/analytics",
    tags=["Analytics"],
)

app.include_router(
    disagreements_router,
    prefix="/disagreements",
    tags=["Reviewer Disagreements"],
)

app.include_router(
    audit_router,
    prefix="/audit-logs",
    tags=["Audit Logs"],
)


@app.get("/")
def root():
    return {
        "message": "AI Evaluation Platform API",
        "status": "running",
        "version": "0.1.0",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "ai-evaluation-platform",
    }


@app.get("/dashboard")
def dashboard():
    return FileResponse("app/static/dashboard.html")
