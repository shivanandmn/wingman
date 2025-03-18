"""
API v1 package initialization.
This package contains all the API endpoints for version 1 of the API.
"""
from app.api.v1 import health, agent, ai_wingman

__all__ = ["health", "agent", "ai_wingman"]
