"""
Test module for the AgentManager class.
"""
import os
import unittest
from unittest.mock import patch, MagicMock

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from wingman import AgentManager


class TestAgentManager(unittest.TestCase):
    """
    Test case for the AgentManager class.
    """
    
    @patch('wingman.core.agent_manager.load_all_configs')
    @patch('wingman.core.agent_manager.ChatOpenAI')
    def test_initialization(self, mock_chat_openai, mock_load_all_configs):
        """
        Test that the AgentManager initializes correctly.
        """
        # Mock the configuration loading
        mock_load_all_configs.return_value = {
            'agents': {
                'test_agent': {
                    'role': 'Test Agent',
                    'goal': 'Test Goal',
                    'backstory': 'Test Backstory',
                }
            },
            'tasks': {
                'test_task': {
                    'description': 'Test Description',
                    'expected_output': 'Test Output',
                    'agent': 'test_agent',
                }
            },
            'crew': {
                'test_crew': {
                    'agents': ['test_agent'],
                    'tasks': ['test_task'],
                    'verbose': True,
                    'process': 'sequential',
                }
            },
            'api': {
                'openai': {
                    'api_key': 'test_key',
                    'model': 'test_model',
                }
            }
        }
        
        # Mock the ChatOpenAI
        mock_chat_openai.return_value = MagicMock()
        
        # Create an agent manager
        agent_manager = AgentManager('test_config_dir')
        
        # Check that the agent manager was initialized correctly
        self.assertEqual(agent_manager.config_dir, 'test_config_dir')
        self.assertEqual(agent_manager.configs, mock_load_all_configs.return_value)
        self.assertIsNotNone(agent_manager.llm)
        self.assertIn('test_agent', agent_manager.agents)
        self.assertIn('test_task', agent_manager.tasks)
        self.assertIn('test_crew', agent_manager.crews)
    
    @patch('wingman.core.agent_manager.load_all_configs')
    @patch('wingman.core.agent_manager.ChatOpenAI')
    def test_update_task_context(self, mock_chat_openai, mock_load_all_configs):
        """
        Test that the update_task_context method works correctly.
        """
        # Mock the configuration loading
        mock_load_all_configs.return_value = {
            'agents': {
                'test_agent': {
                    'role': 'Test Agent',
                    'goal': 'Test Goal',
                    'backstory': 'Test Backstory',
                }
            },
            'tasks': {
                'test_task': {
                    'description': 'Test {topic}',
                    'expected_output': 'Test Output for {topic}',
                    'agent': 'test_agent',
                }
            },
            'crew': {
                'test_crew': {
                    'agents': ['test_agent'],
                    'tasks': ['test_task'],
                    'verbose': True,
                    'process': 'sequential',
                }
            },
            'api': {
                'openai': {
                    'api_key': 'test_key',
                    'model': 'test_model',
                }
            }
        }
        
        # Mock the ChatOpenAI
        mock_chat_openai.return_value = MagicMock()
        
        # Create an agent manager
        agent_manager = AgentManager('test_config_dir')
        
        # Update the task context
        agent_manager.update_task_context({'topic': 'AI Ethics'})
        
        # Check that the context was updated correctly
        self.assertEqual(agent_manager.context, {'topic': 'AI Ethics'})
        
        # Check that the task description was formatted correctly
        self.assertEqual(agent_manager.tasks['test_task'].description, 'Test AI Ethics')
        self.assertEqual(agent_manager.tasks['test_task'].expected_output, 'Test Output for AI Ethics')


if __name__ == '__main__':
    unittest.main()
