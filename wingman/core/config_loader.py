"""
Configuration loader module.
This module contains utility functions for loading YAML configurations.
"""
import os
import yaml
from typing import Dict, Any, Optional
import re


def load_yaml_config(file_path: str) -> Dict[str, Any]:
    """
    Load YAML configuration from a file.
    
    Args:
        file_path (str): Path to the YAML file
        
    Returns:
        Dict[str, Any]: Loaded configuration
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Configuration file not found: {file_path}")
    
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    
    # Process environment variables in the config
    config = _process_env_vars(config)
    
    return config


def _process_env_vars(config: Any) -> Any:
    """
    Process environment variables in the configuration.
    
    Args:
        config (Any): Configuration to process
        
    Returns:
        Any: Processed configuration
    """
    if isinstance(config, dict):
        return {key: _process_env_vars(value) for key, value in config.items()}
    elif isinstance(config, list):
        return [_process_env_vars(item) for item in config]
    elif isinstance(config, str):
        # Replace ${ENV_VAR} with the value of the environment variable
        pattern = r'\${([^}]+)}'
        matches = re.findall(pattern, config)
        
        if matches:
            result = config
            for match in matches:
                env_value = os.environ.get(match)
                if env_value is not None:
                    result = result.replace(f'${{{match}}}', env_value)
            return result
        return config
    else:
        return config


def load_all_configs(config_dir: str) -> Dict[str, Dict[str, Any]]:
    """
    Load all YAML configurations from a directory.
    
    Args:
        config_dir (str): Path to the configuration directory
        
    Returns:
        Dict[str, Dict[str, Any]]: Dictionary of loaded configurations
    """
    configs = {}
    
    for file_name in os.listdir(config_dir):
        if file_name.endswith('.yml') or file_name.endswith('.yaml'):
            file_path = os.path.join(config_dir, file_name)
            config_name = os.path.splitext(file_name)[0]
            config_data = load_yaml_config(file_path)
            
            # Extract the content from the top-level key if it exists
            # For example, from agents.yml, extract the 'agents' key content
            if config_name in config_data:
                configs[config_name] = config_data[config_name]
            else:
                # If the top-level key doesn't match the filename, use the whole config
                configs[config_name] = config_data
    
    print(f"Loaded configs: {configs}")
    return configs
