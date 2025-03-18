"""
Wingman package.
This package contains the agentic architecture components for the Wingman application.

The package provides a simple way to create and orchestrate AI agents using
YAML configuration files. It uses the CrewAI library to create agents, tasks,
and crews that can work together to accomplish complex tasks.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Try to load .env file from different possible locations
possible_env_paths = [
    Path.cwd() / '.env',                    # Current working directory
    Path(__file__).parent.parent / '.env',  # Project root (assuming wingman is a subdirectory)
    Path(__file__).parent / '.env',         # Inside wingman directory
]

# Try each path until we find a .env file
for env_path in possible_env_paths:
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
        break

from wingman.core.agent_manager import AgentManager
from wingman.core.config_loader import load_yaml_config, load_all_configs

__all__ = ["AgentManager", "load_yaml_config", "load_all_configs"]
