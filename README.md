# Streamlit Agent MVP

A minimal Streamlit application that demonstrates an LLM agent capable of planning, reasoning (chain-of-thought), and acting (tool calls) using OpenAI's Chat API.

## Overview

This project implements a simple agent that:
1. **Plans** - Decomposes user tasks into numbered subtasks
2. **Thinks** - Uses chain-of-thought reasoning for each subtask
3. **Acts** - Executes actions (like search) and observes results
4. **Answers** - Provides a final answer based on the execution

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   User      │     │  Streamlit  │     │   Agent     │
│   Input     │────▶│     UI      │────▶│   Logic     │
└─────────────┘     └─────────────┘     └─────────────┘
                            │                    │
                            ▼                    ▼
                    ┌─────────────┐     ┌─────────────┐
                    │   Display   │     │   OpenAI    │
                    │  Plan/Log   │◀────│     API     │
                    └─────────────┘     └─────────────┘

Agent Flow:
1. PLAN: Task → List of Subtasks
2. For each subtask:
   - THOUGHT: Reason about approach
   - ACTION: Execute tool (if needed)
   - OBSERVATION: Capture result
3. ANSWER: Final response
```

## Installation

1. Clone the repository:
```bash
git clone <repo-url>
cd streamlit-agent-mvp
```

2. Install dependencies:
```bash
pip install .
```

3. Set your OpenAI API key:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

## Usage

Run the Streamlit app:
```bash
streamlit run main.py
```

## Example

**Input:** "Get current price of Bitcoin"

**Plan:**
1. Identify the ticker symbol
2. Search current price
3. Format the final answer

**Log:**
- PlanItem: Identify the ticker symbol
- Thought: To start, I need to know Bitcoin's ticker
- Action: Search("Bitcoin ticker symbol")
- Observation: "BTC"
- PlanItem: Search current price
- Thought: Now fetch the current price
- Action: Search("current price of BTC")
- Observation: "It's $54,000"
- PlanItem: Format the final answer
- Thought: I'll write the answer clearly
- Final Answer: "The current price of Bitcoin (BTC) is $54,000"

## Project Structure

```
streamlit-agent-mvp/
├── README.md          # This file
├── pyproject.toml     # Project configuration
├── main.py            # Streamlit UI
├── agent.py           # Agent orchestration logic
├── parser.py          # Response parsing utilities
└── tests/
    └── test_parser.py # Unit tests
```

## Requirements

- Python 3.10+
- Streamlit >= 1.25.0
- OpenAI >= 1.82.0