"""
AI Wingman API endpoints.
This module contains API endpoints for the AI Wingman conflict resolution system.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional

from wingman.ai_wingman import SessionManager
from wingman.ai_wingman.session_manager import (
    EmotionAnalysis, 
    PartnerResponse, 
    CounselorResponse, 
    EncouragerResponse, 
    TherapeuticInteraction
)

# Create a global session manager
session_manager = SessionManager()


class ConversationRequest(BaseModel):
    """
    Conversation request model.
    
    Attributes:
        transcript (str): Transcript of the conversation
        conflict_types (List[str]): Types of conflicts identified
        partner_a_background (str): Background information about partner A
        partner_b_background (str): Background information about partner B
    """
    transcript: str
    conflict_types: List[str]
    partner_a_background: str
    partner_b_background: str


class EmotionAnalysisResponse(EmotionAnalysis):
    """Emotion analysis response model extending the base EmotionAnalysis model."""
    pass


class PartnerResponseModel(PartnerResponse):
    """Partner response model extending the base PartnerResponse model."""
    pass


class CounselorResponseModel(CounselorResponse):
    """Counselor response model extending the base CounselorResponse model."""
    pass


class EncouragerResponseModel(EncouragerResponse):
    """Encourager response model extending the base EncouragerResponse model."""
    pass


class ConversationResponse(BaseModel):
    """
    Enhanced conversation response model for the new agent architecture.
    
    Attributes:
        emotion_analysis (EmotionAnalysisResponse): Analysis of emotional tones and triggers
        partner_a_response (PartnerResponseModel): Partner A's perspective and potential responses
        partner_b_response (PartnerResponseModel): Partner B's perspective and potential responses
        counselor_response (CounselorResponseModel): Counselor's analysis and mediation
        encourager_response (EncouragerResponseModel): Encourager's reinforcement and motivation
        integrated_dialogue (str): Complete integrated therapeutic dialogue
    """
    emotion_analysis: EmotionAnalysisResponse
    partner_a_response: PartnerResponseModel
    partner_b_response: PartnerResponseModel
    counselor_response: CounselorResponseModel
    encourager_response: EncouragerResponseModel
    integrated_dialogue: str


# For backward compatibility
class LegacyConversationResponse(BaseModel):
    """
    Legacy conversation response model for backward compatibility.
    
    Attributes:
        conflict_analysis (str): Analysis of the conflict
        dialogue_script (str): Dialogue for participants to read aloud
        empathy_guidance (str): Guidance for building empathy
        resolution_strategies (str): Strategies for resolving the conflict
    """
    conflict_analysis: str
    dialogue_script: str
    empathy_guidance: str
    resolution_strategies: str


router = APIRouter()


@router.post("/conversation", response_model=ConversationResponse)
async def process_conversation(request: ConversationRequest) -> ConversationResponse:
    """
    Process a conversation for conflict resolution using the new agent architecture.
    
    Args:
        request (ConversationRequest): Conversation request
        
    Returns:
        ConversationResponse: Enhanced conversation response with structured results
    """
    try:
        # Process the transcript
        results = session_manager.process_conversation(
            transcript=request.transcript,
            conflict_types=request.conflict_types,
            partner_a_background=request.partner_a_background,
            partner_b_background=request.partner_b_background
        )
        
        # Create the response with structured data
        return ConversationResponse(
            emotion_analysis=EmotionAnalysisResponse(**results["emotion_analysis"]),
            partner_a_response=PartnerResponseModel(**results["partner_a_response"]),
            partner_b_response=PartnerResponseModel(**results["partner_b_response"]),
            counselor_response=CounselorResponseModel(**results["counselor_response"]),
            encourager_response=EncouragerResponseModel(**results["encourager_response"]),
            integrated_dialogue=results["integrated_dialogue"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/conversation/legacy", response_model=LegacyConversationResponse)
async def process_conversation_legacy(request: ConversationRequest) -> LegacyConversationResponse:
    """
    Process a conversation for conflict resolution using the legacy format.
    This endpoint is provided for backward compatibility.
    
    Args:
        request (ConversationRequest): Conversation request
        
    Returns:
        LegacyConversationResponse: Legacy conversation response with results
    """
    try:
        # Process the transcript
        results = session_manager.process_conversation(
            transcript=request.transcript,
            conflict_types=request.conflict_types,
            partner_a_background=request.partner_a_background,
            partner_b_background=request.partner_b_background
        )
        
        # Extract relevant information for legacy format
        counselor_analysis = results["counselor_response"].get("analysis", "")
        partner_a_perspective = results["partner_a_response"].get("perspective", "")
        partner_b_perspective = results["partner_b_response"].get("perspective", "")
        
        # Combine information for legacy format
        conflict_analysis = f"Counselor Analysis: {counselor_analysis}\n\n"
        conflict_analysis += f"Partner A Perspective: {partner_a_perspective}\n\n"
        conflict_analysis += f"Partner B Perspective: {partner_b_perspective}"
        
        dialogue_script = results["integrated_dialogue"]
        
        empathy_guidance = results["counselor_response"].get("guidance", "")
        
        encourager_strategies = results["encourager_response"].get("motivation_strategies", "")
        counselor_guidance = results["counselor_response"].get("guidance", "")
        resolution_strategies = f"Motivation Strategies: {encourager_strategies}\n\nCounselor Guidance: {counselor_guidance}"
        
        return LegacyConversationResponse(
            conflict_analysis=conflict_analysis,
            dialogue_script=dialogue_script,
            empathy_guidance=empathy_guidance,
            resolution_strategies=resolution_strategies
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
