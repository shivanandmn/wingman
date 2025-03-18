"""
Health check endpoints.
This module contains health check endpoints for the application.
"""
from fastapi import APIRouter
from pydantic import BaseModel


class HealthResponse(BaseModel):
    """
    Health check response model.
    
    Attributes:
        status (str): Status of the application
    """
    status: str


router = APIRouter()


@router.get("/", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Health check endpoint.
    
    Returns:
        HealthResponse: Health check response with status "ok"
    """
    return HealthResponse(status="ok")
