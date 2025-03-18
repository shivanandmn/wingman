"""
Test script for the AI Wingman API endpoint.
"""
import os
import sys
import requests
import json
from pathlib import Path

# Add the parent directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_ai_wingman_endpoint():
    """
    Test the AI Wingman endpoint.
    """
    # API endpoint URL (assuming the API is running locally)
    url = "http://localhost:8000/api/v1/ai-wingman/conversation"
    
    # Sample data
    data = {
        "transcript": """
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
        """,
        "conflict_types": ["Household responsibilities", "Communication breakdown", "Feeling unappreciated"],
        "partner_a_background": """
        Partner A grew up in a very organized household where chores were strictly divided.
        They value cleanliness and order, and feel that maintaining the home is a shared responsibility.
        They work full-time and feel overwhelmed by the household workload.
        They tend to be direct in communication and sometimes come across as critical.
        """,
        "partner_b_background": """
        Partner B grew up in a more relaxed household where chores were done as needed rather than on a schedule.
        They value spontaneity and don't notice mess in the same way as Partner A.
        They also work full-time and feel their contributions are undervalued.
        They tend to avoid conflict and can become defensive when criticized.
        """
    }
    
    # Send the request
    try:
        response = requests.post(url, json=data)
        
        # Check if the request was successful
        if response.status_code == 200:
            result = response.json()
            print("\n=== CONFLICT ANALYSIS ===")
            print(result["conflict_analysis"])
            
            print("\n=== DIALOGUE SCRIPT ===")
            print(result["dialogue_script"])
            
            print("\n=== EMPATHY GUIDANCE ===")
            print(result["empathy_guidance"])
            
            print("\n=== RESOLUTION STRATEGIES ===")
            print(result["resolution_strategies"])
            
            print("\nAPI test successful!")
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    test_ai_wingman_endpoint()
