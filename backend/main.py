"""
InternMatch AI – FastAPI Authoritative Backend.
Entrypoint for API routers, database lifecycle, and system health.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from backend.config import settings
from backend.database.connection import init_db, AsyncSessionLocal
from backend.database.repository import DataRepository

from backend.routers import (
    profile, internships, skill_gap, roadmap, interview, readiness, applications, dashboard
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize tables and seed data
    await init_db()
    async with AsyncSessionLocal() as session:
        repo = DataRepository(session)
        await repo.seed_initial_data_if_needed()
    yield
    # Shutdown

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Explainable, adaptive, end-to-end AI internship recommendation and readiness platform.",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health Check
@app.get("/api/health", tags=["System"])
async def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "database": "connected"
    }

# Register API Routers
app.include_router(profile.router, prefix=settings.API_V1_PREFIX)
app.include_router(internships.router, prefix=settings.API_V1_PREFIX)
app.include_router(skill_gap.router, prefix=settings.API_V1_PREFIX)
app.include_router(roadmap.router, prefix=settings.API_V1_PREFIX)
app.include_router(interview.router, prefix=settings.API_V1_PREFIX)
app.include_router(readiness.router, prefix=settings.API_V1_PREFIX)
app.include_router(applications.router, prefix=settings.API_V1_PREFIX)
app.include_router(dashboard.router, prefix=settings.API_V1_PREFIX)

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
