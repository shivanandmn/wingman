# Wingman API

A FastAPI-based API project with an agentic architecture using CrewAI that is Docker-deployable.

## Project Structure

```
wingman/
├── app/                    # Main application package
│   ├── api/                # API endpoints
│   │   ├── v1/             # API version 1
│   │   │   ├── health.py   # Health check endpoints
│   │   │   ├── agent.py    # Agent endpoints
│   │   ├── routes.py       # API routes
│   ├── core/               # Core functionality
│   │   ├── config.py       # Configuration settings
│   ├── models/             # Database models
│   ├── schemas/            # Pydantic schemas
│   ├── services/           # Business logic
│   ├── utils/              # Utility functions
│   ├── tests/              # Tests
│   ├── main.py             # Main application entry point
├── wingman/                # Agentic architecture package
│   ├── config/             # YAML configuration files
│   │   ├── agents.yml      # Agent configurations
│   │   ├── tasks.yml       # Task configurations
│   │   ├── crew.yml        # Crew configurations
│   │   ├── api.yml         # API configurations
│   ├── core/               # Core functionality
│   │   ├── agent_manager.py # Agent manager
│   │   ├── config_loader.py # Configuration loader
├── .env.example            # Example environment variables
├── docker-compose.yml      # Docker Compose configuration
├── Dockerfile              # Docker configuration
├── README.md               # Project documentation
├── requirements.txt        # Python dependencies
├── setup.py                # Setup script for the wingman package
```

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.11 or higher (for local development)

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd wingman
   ```

2. Create a `.env` file from the example:
   ```
   cp .env.example .env
   ```

3. Build and run the Docker container:
   ```
   docker-compose up --build
   ```

4. The API will be available at http://localhost:8000/api/v1

### Local Development

1. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   uvicorn app.main:app --reload
   ```

## API Documentation

Once the application is running, you can access the API documentation at:

- Swagger UI: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc

## Testing

To run tests:

```
pytest
```

## Agentic Architecture

The project includes an agentic architecture built with CrewAI that allows you to create and orchestrate AI agents to perform complex tasks. The architecture is defined using YAML configuration files and is separated from the main application logic.

### Configuration Files

- **agents.yml**: Defines the agents, their roles, goals, and backstories.
- **tasks.yml**: Defines the tasks that agents can perform, including descriptions and expected outputs.
- **crew.yml**: Defines crews of agents that work together to accomplish a set of tasks.
- **api.yml**: Defines API configurations, including OpenAI API settings.

### YAML Configuration Format

#### agents.yml
```yaml
# Agent configurations
agents:
  researcher:
    name: Research Agent
    role: Researcher
    goal: Find and analyze information on specific topics
    backstory: You are an expert researcher with a knack for finding relevant information quickly and efficiently.
    verbose: true
    allow_delegation: true
    tools: []
```

#### tasks.yml
```yaml
# Task configurations
tasks:
  research_task:
    description: Research {topic} and gather key information
    expected_output: Comprehensive research notes on {topic}
    agent: researcher
    async_execution: false
```

#### crew.yml
```yaml
# Crew configuration
crew:
  content_creation_crew:
    name: Content Creation Crew
    description: A crew of agents that work together to research, write, and review content
    agents:
      - researcher
      - writer
      - reviewer
    tasks:
      - research_task
      - writing_task
      - review_task
    verbose: true
    process:
      sequential: true  # Execute tasks sequentially
    max_rpm: 10  # Rate limit for API calls
```

### Using the Agentic Architecture

To use the agentic architecture in your application:

1. Install the wingman package:
   ```
   pip install -e .
   ```

2. Import the AgentManager:
   ```python
   from wingman import AgentManager
   ```

3. Create an agent manager with your configuration directory:
   ```python
   agent_manager = AgentManager("path/to/config/directory")
   ```

4. Update the task context and run a crew:
   ```python
   agent_manager.update_task_context({"topic": "AI Ethics"})
   result = agent_manager.run_crew("content_creation_crew")
   ```

### How It Works

The agentic architecture works as follows:

1. **Configuration Loading**: The `AgentManager` loads YAML configuration files from the specified directory.

2. **Agent Creation**: Agents are created directly from the configurations in `agents.yml`.

3. **Task Creation**: Tasks are created from the configurations in `tasks.yml` and assigned to the appropriate agents.

4. **Crew Creation**: Crews are created from the configurations in `crew.yml`, combining agents and tasks.

5. **Context Substitution**: When you provide a context (e.g., `{"topic": "AI Ethics"}`), the placeholders in task descriptions and expected outputs (e.g., `{topic}`) are replaced with the corresponding values.

6. **Execution**: When you run a crew, the agents perform their assigned tasks in the specified order (sequential or parallel).

### API Endpoint

The application includes an API endpoint for using the agentic architecture:

- **POST /api/v1/agent/content**: Create content about a topic using the agent system.
  - Request body: `{"topic": "AI Ethics"}`
  - Response: `{"result": "Generated content..."}`
