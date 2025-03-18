"""
Core package.
This package contains core functionality for the Wingman application.
"""
from wingman.core.agent_manager import AgentManager
from wingman.core.config_loader import load_yaml_config, load_all_configs

__all__ = ["AgentManager", "load_yaml_config", "load_all_configs"]
