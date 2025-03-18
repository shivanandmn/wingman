#!/usr/bin/env python
"""
Check environment variables script.

This script checks if the required environment variables are set
and prints their values (or a placeholder if they're not set).
"""

import os
import sys
from pathlib import Path

# Add the parent directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import after adding to path
from dotenv import load_dotenv

def check_env_vars():
    """Check and print environment variables."""
    # Try to load .env file from current directory
    env_path = Path.cwd() / '.env'
    if env_path.exists():
        print(f"Loading .env from: {env_path}")
        load_dotenv(dotenv_path=env_path)
    else:
        print(f"No .env file found at: {env_path}")
    
    # Check for important environment variables
    important_vars = [
        "OPENAI_API_KEY",
        # Add other important environment variables here
    ]
    
    print("\nEnvironment Variables:")
    print("-" * 50)
    for var in important_vars:
        value = os.environ.get(var)
        if value:
            # Show only first few characters of API keys for security
            if "API_KEY" in var and len(value) > 8:
                display_value = value[:4] + "..." + value[-4:]
            else:
                display_value = value
            print(f"{var}: {display_value} (✓)")
        else:
            print(f"{var}: Not set (✗)")
    
    print("-" * 50)
    
    # Check if wingman can access the environment variables
    try:
        from wingman.core.config_loader import load_yaml_config
        from wingman.core.agent_manager import AgentManager
        
        print("\nTesting config loading:")
        print("-" * 50)
        
        # Try to load the API config
        config_path = Path(__file__).parent.parent / "wingman" / "config" / "api.yml"
        if config_path.exists():
            print(f"Loading config from: {config_path}")
            config = load_yaml_config(str(config_path))
            api_key = config.get('api', {}).get('openai', {}).get('api_key')
            
            if api_key:
                print("API key in config: Found (✓)")
            else:
                print("API key in config: Not found (✗)")
        else:
            print(f"Config file not found at: {config_path}")
    except Exception as e:
        print(f"Error testing config: {e}")

if __name__ == "__main__":
    check_env_vars()