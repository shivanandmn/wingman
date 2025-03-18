"""
Configuration settings for the application.
This module contains all the configuration settings for the application.
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """
    Application settings class that loads configuration from environment variables.
    
    Attributes:
        API_V1_STR (str): API version prefix
        PROJECT_NAME (str): Name of the project
        PROJECT_DESCRIPTION (str): Description of the project
        VERSION (str): Version of the application
        HOST (str): Host to run the application on
        PORT (int): Port to run the application on
        DEBUG_MODE (bool): Whether to run in debug mode
        ALLOWED_ORIGINS (List[str]): List of allowed origins for CORS
    """
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Wingman API"
    PROJECT_DESCRIPTION: str = "FastAPI based API for Wingman"
    VERSION: str = "0.1.0"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG_MODE: bool = True
    ALLOWED_ORIGINS: List[str] = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create a global settings object
settings = Settings()
