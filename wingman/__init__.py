"""
Wingman package.
This package contains the agentic architecture components for the Wingman application.

The package provides a simple way to create and orchestrate AI agents using
YAML configuration files. It uses the CrewAI library to create agents, tasks,
and crews that can work together to accomplish complex tasks.
"""
from wingman.core.agent_manager import AgentManager
from wingman.core.config_loader import load_yaml_config, load_all_configs

__all__ = ["AgentManager", "load_yaml_config", "load_all_configs"]
