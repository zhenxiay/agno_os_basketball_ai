# Basketball AI Agent

An AI-driven **Basketball Analytics App** built on AgentOS that provides insights, predictions, and analysis for basketball games and player performance.

## Overview

This project combines artificial intelligence with basketball analytics to create an **interactive Agentic AI App** that can analyze games, predict outcomes, and provide detailed insights about players and teams. Built on the AgentOS framework, it leverages machine learning models and a comprehensive knowledge base to deliver accurate and actionable basketball intelligence.

## Demo

![alt text](visuals/basket_intelligence_agno_demo.gif)

## Features

- **🏀 Team & Player statistic insights**: Look behind the scene and offer insights in teams and player statistics  
- **💬 Interactive Agent**: Natural language interface for the analysis
- **📈 Data Visualization**: Contains AI agent which creates visual representations for data analytics
- **🔬 MLflow Integration**: Integrates MlFlow to trace Agent workflow
- **💾 Knowledge Base**: RAG integrated for the Agentd with a vectorized knowledge base (Qdant)

## Prerequisites

- Python 3.11+
- UV package manager (recommended) or pip
- SQLite (included for local data storage)

## Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/zhenxiay/agno_os_basketball_ai
   cd agno_os_basketball_ai
   ```

2. **Install dependencies**:
   ```bash
   # Using UV (recommended)
   uv sync
   
   # Or using pip
   pip install -e .
   ```

3. **Configure environment**:
   ```bash
   cp template.env .env
   # Edit .env with your API keys and configuration
   ```

4. **Run the application**:
   ```bash
   uv run src/main.py
   ```

## Usage

### Interacting with the AI Analytics Team

This Agent OS offers a framework of multiple AI agents for your basketball related analytics requests.

A team coordinator is configured with reasoning tools and acts as the initial entrypoint of user's request.
It analyzes the request, plan subtasks and distributes them to the agents.

Each agent has its own capabilities (toolkit, instructions, memory etc.).
It peroforms its task based on the requests of the team coordinator.

This AI analztics team understands natural language queries about:

- **Player Statistics**: "How does Stephen Curry impact the game in season 2025? Gather his advanced statistics to analyze!"
- **Team Analysis**: "Give me a clustering analysis based on the NBA team's shooting behavor in season 2024!" 
- **Historical Data**: "Who were the top scorers in the 2023 playoffs?"
- **Strategy Insights**: "What's the best defensive strategy against the Warriors this season?"

## Project Structure

```
agno_os_basketball_ai/
├── src/                    # Source code
│   ├── main.py            # Main application entry point
│   ├── agents/            # AI agent implementations
|   ├── teams/.            # AI team (multi agents team) implementations
│   ├── models/            # ML models and data structures
│   ├── analytics/         # Basketball analytics modules
│   └── utils/             # Utility functions
├── tests/                 # Test suite
├── mlruns/                # MLflow experiment tracking
├── visuals/               # Generated charts and visualizations
├── agno.db               # AgentOS configuration and state
├── knowledge_base.db     # Basketball knowledge base
├── template.env          # Environment template
└── pyproject.toml        # Project configuration
```

## Configuration

### Environment Variables

Copy `template.env` to `.env` and configure:

```env

# LLM API Keys
OPENAI_API_KEY=your-api-key

```

### Agent Capabilities

The agent is configured with specialized capabilities for:
- Statistical analysis and trend identification
- Player & Team performance evaluation
- Data Visualization 

## Architecture

### Core Components

- **AgentOS Framework**: Provides the foundation for intelligent agent behavior
- **Basketball Analytics Toolkit**: Foundamental toolkit for the AI agents to get relevant data for the analysis
- **Knowledge Base**: Stores relevant information for the analysis (NBA official statistic glossary) in a vectorized knowledge base and is availiable for agentic search like RAG.

---

**Built with basketball passion and AI innovation** 🏀🤖

*Leveraging AgentOS, MLflow, and modern Python tooling to revolutionize basketball analytics.*
A powerful multi-agent orchestration platform built with the [Agno framework](https://docs.agno.com/) that enables seamless coordination between AI agents to analyze basketball statistic
