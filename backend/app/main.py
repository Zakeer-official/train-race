from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.config import settings
from app.database import init_db
from app.api.trains import router as trains_router
from app.api.stations import router as stations_router
from app.api.races import router as races_router
from app.api.health import router as health_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize DB tables
    await init_db()
    yield
    # Shutdown

app = FastAPI(
    title=settings.APP_NAME,
    description="Real-Time Indian Railway Head-to-Head Train Comparison Platform",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins for local dev and Vercel preview
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(trains_router)
app.include_router(stations_router)
app.include_router(races_router)
app.include_router(health_router)

@app.get("/")
async def root():
    return {
        "service": settings.APP_NAME,
        "status": "online",
        "docs": "/docs",
        "version": "1.0.0"
    }
