# AI Wingman Agentic Architecture

This module provides an agentic architecture for AI-assisted conflict resolution. The system analyzes transcripts of conversations, identifies conflict patterns, and generates structured dialogues for participants to read aloud to each other.

## Architecture Overview

The AI Wingman system consists of four specialized agents:

1. **Conflict Analyzer**: Analyzes conversation transcripts to identify conflict patterns and underlying issues.
2. **Dialogue Generator**: Creates structured dialogues for participants to read to each other based on conflict analysis.
3. **Empathy Coach**: Guides participants to understand each other's perspectives and emotional needs.
4. **Resolution Strategist**: Develops practical strategies for resolving specific types of conflicts.

These agents work together in a sequential process to provide comprehensive conflict resolution assistance.

## Input and Output

### Input
- **Transcript**: A 5-minute transcript of the conversation/conflict
- **Conflict Types**: Categories of conflicts being experienced
- **Personal Background**: Background information about each participant

### Output
- **Conflict Analysis**: Detailed analysis of conflict patterns, underlying issues, and emotional dynamics
- **Dialogue Script**: A script with alternating dialogue lines for each participant to read to each other
- **Empathy Guidance**: Guidance for each participant to better understand the other's perspective
- **Resolution Strategies**: Actionable strategies tailored to the specific situation

## Usage

```python
from wingman.ai_wingman import SessionManager

# Create a session manager
session_manager = SessionManager()

# Process a transcript
results = session_manager.process_conversation(
    transcript="[Transcript of the conversation]",
    conflict_types=["Communication", "Financial disagreements"],
    partner_a_background="[Background information about partner A]",
    partner_b_background="[Background information about partner B]"
)

# Access the results
conflict_analysis = results["conflict_analysis"]
dialogue_script = results["dialogue_script"]
empathy_guidance = results["empathy_guidance"]
resolution_strategies = results["resolution_strategies"]
```

## Configuration

The agents, tasks, and crew are configured using YAML files in the `config` directory:

- `agents.yml`: Defines the agents and their properties
- `tasks.yml`: Defines the tasks assigned to each agent
- `crew.yml`: Defines how the agents work together as a crew

You can customize these configurations to adjust the behavior of the system.
