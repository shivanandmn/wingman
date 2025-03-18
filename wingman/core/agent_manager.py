"""
Agent manager module.
This module contains the AgentManager class for managing agents, tasks, and crews.

The AgentManager class is the main entry point for using the agentic architecture.
It loads YAML configuration files, creates agents, tasks, and crews, and provides
methods for updating task context and running crews.

Example:
    ```python
    from wingman import AgentManager
    
    # Create an agent manager
    agent_manager = AgentManager("path/to/config/directory")
    
    # Update the task context
    agent_manager.update_task_context({"topic": "AI Ethics"})
    
    # Run a crew
    result = agent_manager.run_crew("content_creation_crew")
    ```
"""
import os
from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI

from wingman.core.config_loader import load_all_configs


class AgentManager:
    """
    Manager class for agents, tasks, and crews.
    """
    
    def __init__(self, config_dir: str):
        """
        Initialize the agent manager.
        
        Args:
            config_dir (str): Path to the configuration directory
        """
        self.config_dir = config_dir
        self.configs = load_all_configs(config_dir)
        self.llm = self._create_llm()
        self.agents = {}
        self.tasks = {}
        self.crews = {}
        self.context = {}
        
        self._initialize()
    
    def _create_llm(self) -> Any:
        """
        Create a language model from the API configuration.
        
        Returns:
            Any: Created language model
        """
        api_config = self.configs.get('api', {}).get('openai', {})
        api_key = api_config.get('api_key')
        
        # Check if API key is None or empty
        if not api_key:
            raise ValueError(
                "OpenAI API key not found. Please set the OPENAI_API_KEY environment variable "
                "or create a .env file in the project root with OPENAI_API_KEY=your_api_key_here"
            )
        return ChatOpenAI(
            api_key=api_key,
            model=api_config.get('model', 'gpt-4o-mini'),
            temperature=api_config.get('temperature', 0.7),
            max_tokens=api_config.get('max_tokens', 4000)
        )
    
    def _create_agents(self):
        """
        Create agents from configurations.
        
        Returns:
            Dict[str, Agent]: Dictionary of created agents
        """
        agents = {}
        agents_config = self.configs.get('agents', {})
        
        print(f"Agent config: {agents_config}")
        
        for agent_id, agent_data in agents_config.items():
            print(f"Creating agent {agent_id}: {agent_data}")
            
            # Ensure required fields have values
            role = agent_data.get('role')
            print(f"Role: {role}")
            
            if not role and 'name' in agent_data:
                role = agent_data.get('name')  # Use name as fallback for role
                print(f"Using name as role: {role}")
            
            # If role is still None, provide a default
            if role is None:
                role = "Agent"  # Default role
                print(f"Using default role: {role}")
            
            goal = agent_data.get('goal')
            if not goal:
                goal = f"Perform tasks as a {role} agent"
                print(f"Using default goal: {goal}")
                
            backstory = agent_data.get('backstory')
            if not backstory:
                backstory = f"You are a {role} agent designed to help with various tasks."
                print(f"Using default backstory: {backstory}")
            
            print(f"Final agent values - role: {role}, goal: {goal}, backstory: {backstory}")
            
            agents[agent_id] = Agent(
                role=role,
                goal=goal,
                backstory=backstory,
                verbose=agent_data.get('verbose', True),
                allow_delegation=agent_data.get('allow_delegation', True),
                tools=agent_data.get('tools', []),
                llm=self.llm
            )
        
        return agents
    
    def _format_with_context(self, text: str) -> str:
        """
        Format text with context variables.
        
        Args:
            text (str): Text to format
            
        Returns:
            str: Formatted text
        """
        if not self.context:
            return text
            
        for key, value in self.context.items():
            text = text.replace(f"{{{key}}}", str(value))
            
        return text
    
    def _create_tasks(self):
        """
        Create tasks from configurations.
        
        Returns:
            Dict[str, Task]: Dictionary of created tasks
        """
        tasks = {}
        tasks_config = self.configs.get('tasks', {})
        
        for task_id, task_data in tasks_config.items():
            agent_id = task_data.get('agent')
            agent = self.agents.get(agent_id)
            
            if not agent:
                raise ValueError(f"Agent '{agent_id}' not found for task '{task_id}'")
            
            # Format description and expected output with context
            description = self._format_with_context(task_data.get('description', ''))
            expected_output = self._format_with_context(task_data.get('expected_output', ''))
            
            tasks[task_id] = Task(
                description=description,
                expected_output=expected_output,
                agent=agent,
                async_execution=task_data.get('async_execution', False)
            )
        
        return tasks
    
    def _create_crews(self):
        """
        Create crews from configurations.
        
        Returns:
            Dict[str, Crew]: Dictionary of created crews
        """
        crews = {}
        crews_config = self.configs.get('crew', {})
        
        for crew_id, crew_data in crews_config.items():
            # Get the agents for the crew
            crew_agents = []
            for agent_id in crew_data.get('agents', []):
                agent = self.agents.get(agent_id)
                if not agent:
                    raise ValueError(f"Agent '{agent_id}' not found for crew '{crew_id}'")
                crew_agents.append(agent)
            
            # Get the tasks for the crew
            crew_tasks = []
            for task_id in crew_data.get('tasks', []):
                task = self.tasks.get(task_id)
                if not task:
                    raise ValueError(f"Task '{task_id}' not found for crew '{crew_id}'")
                crew_tasks.append(task)
            
            # Handle process parameter (can be a string or a dict)
            process_param = crew_data.get('process', 'sequential')
            if isinstance(process_param, dict):
                process = process_param.get('sequential', True)
            else:
                process = process_param
                
            crews[crew_id] = Crew(
                agents=crew_agents,
                tasks=crew_tasks,
                verbose=crew_data.get('verbose', True),
                process=process,
                max_rpm=crew_data.get('max_rpm', 20)
            )
        
        return crews
    
    def _initialize(self):
        """
        Initialize agents, tasks, and crews from configurations.
        """
        # Create agents
        self.agents = self._create_agents()
        
        # Create tasks
        self.tasks = self._create_tasks()
        
        # Create crews
        self.crews = self._create_crews()
    
    def get_crew(self, crew_id: str):
        """
        Get a crew by ID.
        
        Args:
            crew_id (str): ID of the crew
            
        Returns:
            Any: Crew with the specified ID
        """
        return self.crews.get(crew_id)
    
    def update_task_context(self, context: Dict[str, Any]):
        """
        Update the context for all tasks.
        
        Args:
            context (Dict[str, Any]): Context variables for the tasks
        """
        # Update context
        self.context = context
        
        # Recreate tasks with the new context
        self.tasks = self._create_tasks()
        
        # Recreate crews with the new tasks
        self.crews = self._create_crews()
    
    def run_crew(self, crew_id: str):
        """
        Run a crew by ID.
        
        Args:
            crew_id (str): ID of the crew
            
        Returns:
            Any: Result of the crew execution
        """
        crew = self.get_crew(crew_id)
        if not crew:
            raise ValueError(f"Crew '{crew_id}' not found")
        
        return crew.kickoff()
