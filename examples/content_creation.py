#!/usr/bin/env python
"""
Example script for using the wingman package to create content.

This script demonstrates how to use the AgentManager to create content
about a specified topic using a crew of AI agents.
"""
import os
import sys
import argparse
from dotenv import load_dotenv

# Add the parent directory to sys.path to import the wingman package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from wingman import AgentManager


def main():
    """
    Main function to run the content creation example.
    """
    # Load environment variables from .env file
    load_dotenv()
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Create content about a topic using AI agents")
    parser.add_argument("topic", help="Topic to create content about")
    args = parser.parse_args()
    
    # Get the path to the config directory
    config_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "wingman/config")
    
    # Create an agent manager
    print(f"Creating agent manager with config directory: {config_dir}")
    agent_manager = AgentManager(config_dir)
    
    # Update the task context with the topic
    print(f"Updating task context with topic: {args.topic}")
    agent_manager.update_task_context({"topic": args.topic})
    
    # Run the content creation crew
    print("Running content creation crew...")
    result = agent_manager.run_crew("content_creation_crew")
    
    # Print the result
    print("\nContent Creation Result:")
    print("=" * 80)
    print(result)
    print("=" * 80)


if __name__ == "__main__":
    main()
