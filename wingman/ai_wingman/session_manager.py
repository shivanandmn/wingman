"""
Session Manager module.
This module contains the SessionManager class for managing AI-assisted conflict resolution sessions.
"""

import os
import json
import re
from typing import Dict, Any, List, Optional, Union
from pathlib import Path
from pydantic import BaseModel, Field

from wingman import AgentManager


# Define Pydantic models for structured output
class EmotionAnalysis(BaseModel):
    """Emotion analysis model for structured output from the emotion recognition agent."""
    partner_a_emotions: Dict[str, float] = Field(description="Emotions detected for Partner A with intensity scores (0.0-1.0)")
    partner_b_emotions: Dict[str, float] = Field(description="Emotions detected for Partner B with intensity scores (0.0-1.0)")
    emotional_triggers: List[str] = Field(description="Identified emotional triggers in the conversation")
    recommendations: str = Field(description="Recommendations for addressing the emotional dynamics")


class PartnerResponse(BaseModel):
    """Partner response model for structured output from partner agents."""
    emotional_state: str = Field(description="Current emotional state based on the conversation")
    perspective: str = Field(description="Partner's perspective on the conflict")
    potential_dialogue: str = Field(description="How the partner might respond in this situation")


class CounselorResponse(BaseModel):
    """Counselor response model for structured output from the counselor agent."""
    analysis: str = Field(description="Analysis of the underlying issues and dynamics")
    mediation_dialogue: str = Field(description="Mediation dialogue to help partners communicate better")
    guidance: str = Field(description="Guidance for a more productive conversation")


class EncouragerResponse(BaseModel):
    """Encourager response model for structured output from the encourager agent."""
    positive_observations: str = Field(description="Observations of positive behaviors or intentions")
    reinforcement_dialogue: str = Field(description="Dialogue to reinforce positive actions")
    motivation_strategies: str = Field(description="Strategies to motivate continued positive behavior")


class TherapeuticInteraction(BaseModel):
    """Complete therapeutic interaction model that integrates all agent outputs."""
    emotion_analysis: EmotionAnalysis = Field(description="Analysis of emotional tones and triggers")
    partner_a_response: PartnerResponse = Field(description="Partner A's perspective and potential responses")
    partner_b_response: PartnerResponse = Field(description="Partner B's perspective and potential responses")
    counselor_response: CounselorResponse = Field(description="Counselor's analysis and mediation")
    encourager_response: EncouragerResponse = Field(description="Encourager's reinforcement and motivation")
    integrated_dialogue: str = Field(description="Complete integrated therapeutic dialogue")


class SessionManager:
    """
    Manager class for AI-assisted conflict resolution sessions.
    """
    
    def __init__(self, config_dir: Optional[str] = None):
        """
        Initialize the session manager.
        
        Args:
            config_dir (str, optional): Path to the configuration directory. 
                                       If None, uses the default AI Wingman configs.
        """
        if config_dir is None:
            # Use the default AI Wingman config directory
            module_dir = Path(__file__).parent.parent
            config_dir = os.path.join(module_dir, "config")
        
        self.agent_manager = AgentManager(config_dir)
    
    def process_conversation(self, 
                           transcript: str, 
                           conflict_types: List[str], 
                           partner_a_background: str, 
                           partner_b_background: str) -> Dict[str, Any]:
        """
        Process a conversation transcript and generate therapeutic interaction.
        
        Args:
            transcript (str): The transcript of the couple's conversation
            conflict_types (List[str]): Types of conflicts identified
            partner_a_background (str): Background information about partner A
            partner_b_background (str): Background information about partner B
            
        Returns:
            Dict[str, Any]: The results of the AI Wingman session, including:
                - emotion_analysis: Analysis of emotional tones and triggers
                - partner_a_response: Partner A's perspective and potential responses
                - partner_b_response: Partner B's perspective and potential responses
                - counselor_response: Counselor's analysis and mediation
                - encourager_response: Encourager's reinforcement and motivation
                - integrated_dialogue: Complete integrated therapeutic dialogue
        """
        # Initialize the task context with the provided information
        initial_context = {
            "transcript": transcript,
            "conflict_types": ", ".join(conflict_types),
            "partner_a_background": partner_a_background,
            "partner_b_background": partner_b_background
        }
        
        # Update the task context with the initial information
        self.agent_manager.update_task_context(initial_context)
        
        # Run the AI Wingman crew with the updated context
        print("Running AI Wingman crew...")
        crew_result = self.agent_manager.run_crew("ai_wingman_crew")
        print("AI Wingman crew execution completed.")
        
        # Extract and parse the results using Pydantic models
        emotion_analysis = self._extract_and_parse_task_result(
            crew_result, 
            "analyze_emotions_task", 
            EmotionAnalysis
        )
        
        partner_a_response = self._extract_and_parse_task_result(
            crew_result, 
            "simulate_partner_a_task", 
            PartnerResponse
        )
        
        partner_b_response = self._extract_and_parse_task_result(
            crew_result, 
            "simulate_partner_b_task", 
            PartnerResponse
        )
        
        counselor_response = self._extract_and_parse_task_result(
            crew_result, 
            "provide_counseling_task", 
            CounselorResponse
        )
        
        encourager_response = self._extract_and_parse_task_result(
            crew_result, 
            "provide_encouragement_task", 
            EncouragerResponse
        )
        
        integrated_dialogue = self._extract_task_result(crew_result, "generate_interaction_task")
        
        # Organize the results
        session_results = {
            "emotion_analysis": emotion_analysis.dict() if emotion_analysis else {},
            "partner_a_response": partner_a_response.dict() if partner_a_response else {},
            "partner_b_response": partner_b_response.dict() if partner_b_response else {},
            "counselor_response": counselor_response.dict() if counselor_response else {},
            "encourager_response": encourager_response.dict() if encourager_response else {},
            "integrated_dialogue": integrated_dialogue
        }
        
        return session_results
    
    def _extract_task_result(self, crew_result: Any, task_id: str, agent_filter: Optional[str] = None) -> str:
        """
        Extract the raw result of a specific task from the crew result.
        
        Args:
            crew_result (Any): The result of running the crew
            task_id (str): The ID of the task to extract
            agent_filter (str, optional): Filter results by agent name
            
        Returns:
            str: The raw result of the task
        """
        # Print the crew result for debugging
        print(f"DEBUG - Crew result type: {type(crew_result)}")
        
        # Handle different result formats based on the CrewAI version
        if isinstance(crew_result, dict):
            # Try to extract the result from the task_results dictionary
            if "task_results" in crew_result:
                for task_result in crew_result.get("task_results", []):
                    if task_result.get("task_id") == task_id:
                        if agent_filter and task_result.get("agent") != agent_filter:
                            continue
                        return task_result.get("result", "")
            # Try to extract the result from the tasks dictionary
            elif "tasks" in crew_result:
                for task_result in crew_result.get("tasks", []):
                    if task_result.get("id") == task_id or task_result.get("task_id") == task_id:
                        if agent_filter and task_result.get("agent") != agent_filter:
                            continue
                        return task_result.get("output", "") or task_result.get("result", "")
            # Try to extract the result directly
            elif task_id in crew_result:
                return crew_result.get(task_id, "")
        # Handle list format
        elif isinstance(crew_result, list):
            for task_result in crew_result:
                if isinstance(task_result, dict):
                    if task_result.get("task_id") == task_id or task_result.get("id") == task_id:
                        if agent_filter and task_result.get("agent") != agent_filter:
                            continue
                        return task_result.get("result", "") or task_result.get("output", "")
        # Handle string format
        elif isinstance(crew_result, str):
            # If the result is a string, try to extract the relevant section
            import re
            section_patterns = {
                "analyze_emotions_task": r'===\s*EMOTION ANALYSIS\s*===(.*?)(?:===\s*|$)',
                "simulate_partners_task": r'===\s*PARTNER SIMULATION\s*===(.*?)(?:===\s*|$)',
                "provide_counseling_task": r'===\s*COUNSELING\s*===(.*?)(?:===\s*|$)',
                "provide_encouragement_task": r'===\s*ENCOURAGEMENT\s*===(.*?)(?:===\s*|$)',
                "generate_interaction_task": r'===\s*INTEGRATED DIALOGUE\s*===(.*?)(?:===\s*|$)'
            }
            
            if task_id in section_patterns:
                match = re.search(section_patterns[task_id], crew_result, re.DOTALL)
                if match:
                    # If we have an agent filter, try to find the specific agent's output
                    if agent_filter:
                        agent_pattern = rf'{agent_filter}\s*[:=]\s*(.*?)(?:===|$)'
                        agent_match = re.search(agent_pattern, match.group(1), re.DOTALL | re.IGNORECASE)
                        if agent_match:
                            return agent_match.group(1).strip()
                    return match.group(1).strip()
        
        # If task result not found or in an unexpected format, return empty string
        return ""
    
    def _extract_and_parse_task_result(self, 
                                     crew_result: Any, 
                                     task_id: str, 
                                     model_class: type[BaseModel],
                                     agent_filter: Optional[str] = None) -> Optional[BaseModel]:
        """
        Extract and parse the result of a specific task from the crew result using a Pydantic model.
        
        Args:
            crew_result (Any): The result of running the crew
            task_id (str): The ID of the task to extract
            model_class (type[BaseModel]): The Pydantic model class to use for parsing
            agent_filter (str, optional): Filter results by agent name
            
        Returns:
            Optional[BaseModel]: The parsed result as a Pydantic model instance, or None if parsing fails
        """
        # Extract the raw result
        raw_result = self._extract_task_result(crew_result, task_id, agent_filter)
        
        if not raw_result:
            return None
        
        # Try to parse the result as JSON
        try:
            # First, try to find a JSON object in the raw result
            json_match = re.search(r'\{.*\}', raw_result, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                data = json.loads(json_str)
                return model_class(**data)
            
            # If no JSON object found, try to parse the entire result as JSON
            data = json.loads(raw_result)
            return model_class(**data)
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error parsing JSON: {e}")
            
            # If JSON parsing fails, try to extract structured data using regex
            try:
                # Create an empty dict to hold the extracted fields
                extracted_data = {}
                
                # Get all field names from the model
                field_names = list(model_class.__annotations__.keys())
                
                # Try to extract each field using regex
                for field_name in field_names:
                    # Convert field_name from snake_case to title case for regex matching
                    display_name = " ".join(word.capitalize() for word in field_name.split("_"))
                    
                    # Try different patterns for extraction
                    patterns = [
                        rf'{field_name}\s*[:=]\s*[\"\'](.*?)[\"\']',  # field_name: "value"
                        rf'{field_name}\s*[:=]\s*(.*?)(?:\n|$)',     # field_name: value
                        rf'{display_name}\s*[:=]\s*[\"\'](.*?)[\"\']',  # Display Name: "value"
                        rf'{display_name}\s*[:=]\s*(.*?)(?:\n|$)'      # Display Name: value
                    ]
                    
                    for pattern in patterns:
                        match = re.search(pattern, raw_result, re.IGNORECASE | re.DOTALL)
                        if match:
                            extracted_data[field_name] = match.group(1).strip()
                            break
                
                # Special handling for dictionary and list fields
                for field_name in field_names:
                    field_type = model_class.__annotations__[field_name]
                    
                    # Handle dictionary fields (like emotions)
                    if 'Dict' in str(field_type) and field_name in extracted_data:
                        try:
                            # Try to parse as JSON
                            if extracted_data[field_name].startswith('{') and extracted_data[field_name].endswith('}'):
                                extracted_data[field_name] = json.loads(extracted_data[field_name])
                            else:
                                # Try to parse as key-value pairs
                                emotion_dict = {}
                                emotion_pairs = re.findall(r'([\w\s]+):\s*([0-9.]+)', extracted_data[field_name])
                                for emotion, score in emotion_pairs:
                                    emotion_dict[emotion.strip()] = float(score)
                                if emotion_dict:
                                    extracted_data[field_name] = emotion_dict
                        except Exception as e:
                            print(f"Error parsing dictionary field {field_name}: {e}")
                            extracted_data[field_name] = {}
                    
                    # Handle list fields (like emotional_triggers)
                    elif 'List' in str(field_type) and field_name in extracted_data:
                        try:
                            # Try to parse as JSON
                            if extracted_data[field_name].startswith('[') and extracted_data[field_name].endswith(']'):
                                extracted_data[field_name] = json.loads(extracted_data[field_name])
                            else:
                                # Try to parse as comma-separated values
                                items = [item.strip() for item in extracted_data[field_name].split(',')]
                                if items:
                                    extracted_data[field_name] = items
                        except Exception as e:
                            print(f"Error parsing list field {field_name}: {e}")
                            extracted_data[field_name] = []
                
                # If we've extracted at least some fields, try to create the model
                if extracted_data:
                    # For any missing fields, use empty defaults based on field type
                    for field_name in field_names:
                        if field_name not in extracted_data:
                            field_type = model_class.__annotations__[field_name]
                            if 'Dict' in str(field_type):
                                extracted_data[field_name] = {}
                            elif 'List' in str(field_type):
                                extracted_data[field_name] = []
                            elif 'str' in str(field_type):
                                extracted_data[field_name] = ""
                            elif 'float' in str(field_type) or 'int' in str(field_type):
                                extracted_data[field_name] = 0
                    
                    return model_class(**extracted_data)
            except Exception as e:
                print(f"Error extracting structured data: {e}")
                
                # As a fallback, create an instance with default values
                try:
                    default_values = {}
                    for field_name in field_names:
                        field_type = model_class.__annotations__[field_name]
                        if 'Dict' in str(field_type):
                            default_values[field_name] = {}
                        elif 'List' in str(field_type):
                            default_values[field_name] = []
                        elif 'str' in str(field_type):
                            # Try to extract some content for string fields
                            if field_name == 'analysis' or field_name == 'perspective':
                                default_values[field_name] = raw_result[:500] if len(raw_result) > 500 else raw_result
                            else:
                                default_values[field_name] = ""
                        elif 'float' in str(field_type) or 'int' in str(field_type):
                            default_values[field_name] = 0
                    
                    return model_class(**default_values)
                except Exception as e:
                    print(f"Error creating default model: {e}")
                    return None
        
        return None
