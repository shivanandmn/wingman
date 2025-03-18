"""
Example script for using the AI Wingman module.

This script demonstrates how to use the SessionManager class to process
a transcript of a conversation and generate therapeutic interactions
using the new agent architecture.
"""

import os
import sys
import json
from pathlib import Path

# Add the parent directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from wingman.ai_wingman import SessionManager
from wingman.ai_wingman.session_manager import (
    EmotionAnalysis, 
    PartnerResponse, 
    CounselorResponse, 
    EncouragerResponse
)


def main():
    """
    Run an AI Wingman session example with the new agent architecture.
    """
    # Sample data
    transcript = """
    Partner A: You never help with the housework! I'm always the one cleaning up after everyone.
    Partner B: That's not true! I do plenty around here. You just don't notice it.
    Partner A: Like what? Name one thing you did this week.
    Partner B: I took out the trash yesterday and did the dishes on Tuesday.
    Partner A: That's barely anything compared to what I do every single day!
    Partner B: You always exaggerate. You make it sound like I do nothing at all.
    Partner A: Because it feels that way to me! I'm exhausted from doing everything.
    Partner B: Well maybe if you weren't so controlling about how things get done, I'd do more.
    Partner A: So now it's my fault that you don't help?
    Partner B: I didn't say that. You're twisting my words again!
    """
    
    conflict_types = ["Household responsibilities", "Communication breakdown", "Feeling unappreciated"]
    
    partner_a_background = """
    Partner A grew up in a very organized household where chores were strictly divided.
    They value cleanliness and order, and feel that maintaining the home is a shared responsibility.
    They work full-time and feel overwhelmed by the household workload.
    They tend to be direct in communication and sometimes come across as critical.
    """
    
    partner_b_background = """
    Partner B grew up in a more relaxed household where chores were done as needed rather than on a schedule.
    They value spontaneity and don't notice mess in the same way as Partner A.
    They also work full-time and feel their contributions are undervalued.
    They tend to avoid conflict and can become defensive when criticized.
    """
    
    # Create a session manager
    session_manager = SessionManager()
    
    # Process the transcript
    results = session_manager.process_conversation(
        transcript=transcript,
        conflict_types=conflict_types,
        partner_a_background=partner_a_background,
        partner_b_background=partner_b_background
    )
    
    # Print raw results for debugging
    print("\nRAW RESULTS:")
    print(f"Type of results: {type(results)}")
    print(f"Keys in results: {results.keys() if isinstance(results, dict) else 'Not a dictionary'}")
    
    # Print the formatted results using the new agent architecture
    
    # 1. Emotion Analysis
    print("\n=== EMOTION ANALYSIS ===")
    emotion_analysis = results.get("emotion_analysis", {})
    if emotion_analysis:
        print("\nPartner A Emotions:")
        for emotion, intensity in emotion_analysis.get("partner_a_emotions", {}).items():
            print(f"  {emotion}: {intensity:.2f}")
        
        print("\nPartner B Emotions:")
        for emotion, intensity in emotion_analysis.get("partner_b_emotions", {}).items():
            print(f"  {emotion}: {intensity:.2f}")
        
        print("\nEmotional Triggers:")
        for trigger in emotion_analysis.get("emotional_triggers", []):
            print(f"  - {trigger}")
        
        print("\nRecommendations:")
        print(emotion_analysis.get("recommendations", ""))
    
    # 2. Partner A Response
    print("\n=== PARTNER A RESPONSE ===")
    partner_a = results.get("partner_a_response", {})
    if partner_a:
        print(f"Emotional State: {partner_a.get('emotional_state', '')}\n")
        print(f"Perspective: {partner_a.get('perspective', '')}\n")
        print(f"Potential Dialogue: {partner_a.get('potential_dialogue', '')}\n")
    
    # 3. Partner B Response
    print("\n=== PARTNER B RESPONSE ===")
    partner_b = results.get("partner_b_response", {})
    if partner_b:
        print(f"Emotional State: {partner_b.get('emotional_state', '')}\n")
        print(f"Perspective: {partner_b.get('perspective', '')}\n")
        print(f"Potential Dialogue: {partner_b.get('potential_dialogue', '')}\n")
    
    # 4. Counselor Response
    print("\n=== COUNSELOR RESPONSE ===")
    counselor = results.get("counselor_response", {})
    if counselor:
        print(f"Analysis: {counselor.get('analysis', '')}\n")
        print(f"Mediation Dialogue: {counselor.get('mediation_dialogue', '')}\n")
        print(f"Guidance: {counselor.get('guidance', '')}\n")
    
    # 5. Encourager Response
    print("\n=== ENCOURAGER RESPONSE ===")
    encourager = results.get("encourager_response", {})
    if encourager:
        print(f"Positive Observations: {encourager.get('positive_observations', '')}\n")
        print(f"Reinforcement Dialogue: {encourager.get('reinforcement_dialogue', '')}\n")
        print(f"Motivation Strategies: {encourager.get('motivation_strategies', '')}\n")
    
    # 6. Integrated Dialogue
    print("\n=== INTEGRATED THERAPEUTIC DIALOGUE ===")
    print(results.get("integrated_dialogue", ""))


# Legacy support function for backward compatibility
def legacy_format():
    """
    Demonstrates how to use the legacy format for backward compatibility.
    """
    session_manager = SessionManager()
    
    # Sample data (same as above)
    transcript = """
    Partner A: You never help with the housework! I'm always the one cleaning up after everyone.
    Partner B: That's not true! I do plenty around here. You just don't notice it.
    """
    
    conflict_types = ["Household responsibilities", "Communication breakdown"]
    partner_a_background = "Partner A values cleanliness and order."
    partner_b_background = "Partner B values spontaneity and flexibility."
    
    # Process the transcript
    results = session_manager.process_conversation(
        transcript=transcript,
        conflict_types=conflict_types,
        partner_a_background=partner_a_background,
        partner_b_background=partner_b_background
    )
    
    # Convert to legacy format
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
    
    # Print the legacy format results
    print("\n=== LEGACY FORMAT ===")
    print("\n=== CONFLICT ANALYSIS ===")
    print(conflict_analysis)
    
    print("\n=== DIALOGUE SCRIPT ===")
    print(dialogue_script)
    
    print("\n=== EMPATHY GUIDANCE ===")
    print(empathy_guidance)
    
    print("\n=== RESOLUTION STRATEGIES ===")
    print(resolution_strategies)


if __name__ == "__main__":
    main()
    # Uncomment to run the legacy format example
    # print("\n" + "-"*50)
    # legacy_format()
