# Social Simulation with LLM-based Agents

This project simulates a social environment with LLM-based agents that can generate and spread rumors.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up Together API key:
```bash
export TOGETHER_API_KEY="your_api_key_here"
```

## Project Structure

- `agents/`: Agent-related classes
  - `persona.py`: Persona class with LLM integration
- `memory/`: Memory-related classes
  - `associative_memory.py`: Memory system with semantic search
  - `concept_node.py`: Memory node representation
  - `scratch.py`: Current state storage
- `world/`: World simulation classes
  - `world.py`: Main simulation class
  - `rumor_visor.py`: Rumor management system
- `simulation.py`: Main simulation script

## Running the Simulation

To run the simulation with 5 agents:
```bash
python simulation.py
```

## Features

- LLM-based agent communication
- Semantic memory system
- Rumor generation and spread
- Social distance calculation
- Rumor modification based on agent traits

## Configuration

The simulation can be configured by modifying the agent parameters in `simulation.py`:
- Name, age, and traits
- Lifestyle and social behavior
- Mendacity level (propensity to spread rumors)

## Output

The simulation outputs:
- Agent interactions
- Rumor generation and spread
- Social dynamics
- Memory reflections 