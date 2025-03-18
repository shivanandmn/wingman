"""
API routes module.
This module contains all the API routes for the application.
"""
from fastapi import APIRouter

from app.api.v1 import health, agent

# Create the main API router
api_router = APIRouter()

# Include all routers from different API versions
api_router.include_router(health.router, prefix="/health", tags=["Health"])
api_router.include_router(agent.router, prefix="/agent", tags=["Agent"])
