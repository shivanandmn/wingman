"""
Agent API endpoints.
This module contains API endpoints for the agent system.
"""
import os
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, List, Optional

from wingman import AgentManager


# Create a global agent manager
CONFIG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "wingman/config")
agent_manager = AgentManager(CONFIG_DIR)


class TopicRequest(BaseModel):
    """
    Topic request model.
    
    Attributes:
        topic (str): Topic to research and write about
    """
    topic: str


class AgentResponse(BaseModel):
    """
    Agent response model.
    
    Attributes:
        result (str): Result of the agent execution
    """
    result: str


router = APIRouter()


@router.post("/content", response_model=AgentResponse)
async def create_content(request: TopicRequest) -> AgentResponse:
    """
    Create content about a topic using the agent system.
    
    Args:
        request (TopicRequest): Topic request
        
    Returns:
        AgentResponse: Agent response with the result
    """
    try:
        # Update the task context with the topic
        agent_manager.update_task_context({"topic": request.topic})
        
        # Run the content creation crew
        result = agent_manager.run_crew("content_creation_crew")
        
        return AgentResponse(result=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
