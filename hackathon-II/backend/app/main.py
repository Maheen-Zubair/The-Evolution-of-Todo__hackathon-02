"""
Phase 2 Full-Stack Todo App - FastAPI Application

Main entry point for the backend API.
"""

import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db import create_db_and_tables
from app.routers import tasks_router

# Load environment variables
load_dotenv()

# Get frontend URL for CORS
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup: Create database tables
    create_db_and_tables()
    yield
    # Shutdown: cleanup if needed


# Create FastAPI application
app = FastAPI(
    title="Phase 2 Todo API",
    description="Full-stack todo application REST API with user authentication",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,  # Required for cookies
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "todo-api"}


@app.get("/")
def root():
    """Root endpoint with API information."""
    return {
        "message": "Phase 2 Todo API",
        "docs": "/docs",
        "health": "/health",
    }


# Register routers
app.include_router(tasks_router)
