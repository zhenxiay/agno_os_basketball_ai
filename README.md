# Basketball AI Agent

An intelligent basketball analytics agent built on AgentOS that provides insights, predictions, and analysis for basketball games and player performance.

## Overview

This project combines artificial intelligence with basketball analytics to create an interactive agent that can analyze games, predict outcomes, and provide detailed insights about players and teams. Built on the AgentOS framework, it leverages machine learning models and a comprehensive knowledge base to deliver accurate and actionable basketball intelligence.

## Demo

![alt text](visuals/basketball_agno_os_demo.mp4)

## Features

- **🏀 Game Analysis**: Real-time analysis of basketball games and player statistics
- **📊 Performance Predictions**: ML-powered predictions for player and team performance  
- **💬 Interactive Agent**: Natural language interface for basketball insights and recommendations
- **📈 Data Visualization**: Rich visual representations of basketball data and analytics
- **🔬 MLflow Integration**: Experiment tracking and model management
- **💾 Knowledge Base**: Comprehensive basketball data storage and retrieval

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

### Interacting with the Agent

The basketball AI agent understands natural language queries about:

- **Player Statistics**: "What are LeBron James' shooting percentages this season?"
- **Game Predictions**: "Predict the outcome of Lakers vs Warriors tonight"
- **Team Analysis**: "Show me the Celtics' defensive performance trends"
- **Historical Data**: "Who were the top scorers in the 2023 playoffs?"
- **Strategy Insights**: "What's the best defensive strategy against the Warriors?"

## Project Structure

```
agno_os_basketball_ai/
├── src/                    # Source code
│   ├── main.py            # Main application entry point
│   ├── agents/            # AI agent implementations
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
# API Keys
NBA_API_KEY=your_nba_api_key
SPORTS_API_KEY=your_sports_api_key

# Database Configuration
DATABASE_URL=sqlite:///agno.db
KNOWLEDGE_BASE_URL=sqlite:///knowledge_base.db

# Model Configuration
MODEL_PATH=models/
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Agent Settings
MAX_CONTEXT_LENGTH=4000
TEMPERATURE=0.7
```

### Agent Capabilities

The agent is configured with specialized capabilities for:
- Statistical analysis and trend identification
- Game prediction using historical data
- Player performance evaluation
- Team strategy recommendations
- Real-time game commentary and insights

## Development

### Setting up Development Environment

```bash
# Install development dependencies
uv sync --dev

# Install pre-commit hooks
pre-commit install

# Run tests
uv run pytest

# Run linting
uv run flake8 src/
uv run black src/

# Type checking
uv run mypy src/
```

### MLflow Experiments

Monitor model performance and experiments:

```bash
# Start MLflow UI
mlflow ui

# View experiments at http://localhost:5000
```

### Testing

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src

# Run specific test categories
uv run pytest tests/unit/
uv run pytest tests/integration/
```

## Architecture

### Core Components

- **AgentOS Framework**: Provides the foundation for intelligent agent behavior
- **Basketball Analytics Engine**: Processes game data and generates insights
- **ML Pipeline**: Handles model training, evaluation, and predictions
- **Knowledge Base**: Stores and retrieves basketball-related information
- **Visualization Engine**: Creates charts and visual representations of data

### Data Flow

1. **Data Ingestion**: Basketball data from various APIs and sources
2. **Processing**: Clean, normalize, and enrich the data
3. **Storage**: Store in knowledge base with efficient indexing
4. **Analysis**: Apply ML models and statistical analysis
5. **Response Generation**: Create natural language responses with visualizations

## Performance

> [!NOTE]
> The agent is optimized for basketball analytics workloads with:
> - Sub-second response times for statistical queries
> - Real-time game analysis capabilities
> - Efficient data retrieval from the knowledge base
> - Scalable ML model inference

## Troubleshooting

### Common Issues

**Database Connection Errors**:
```bash
# Verify database files exist
ls -la *.db

# Reset databases if corrupted
rm agno.db knowledge_base.db
python src/main.py --init-db
```

**API Rate Limits**:
- Check your API key quotas
- Implement request throttling in configuration
- Consider caching frequently accessed data

**Memory Issues**:
- Reduce `MAX_CONTEXT_LENGTH` in configuration
- Use smaller embedding models for lower memory usage
- Enable model quantization for inference

## Contributing

We welcome contributions! Please see our contribution guidelines:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-basketball-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing basketball feature'`)
4. **Push** to the branch (`git push origin feature/amazing-basketball-feature`)
5. **Open** a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation for API changes
- Use type hints throughout the codebase
- Ensure all tests pass before submitting PRs

## Roadmap

- [ ] **Advanced Player Tracking**: Integration with player tracking data
- [ ] **Live Game Integration**: Real-time game analysis during broadcasts  
- [ ] **Fantasy Basketball**: Tools for fantasy league analysis
- [ ] **Social Features**: Share insights and predictions with other users
- [ ] **Mobile App**: Native mobile application for on-the-go analysis

## Support

Need help? Here are your options:

- **Issues**: Report bugs or request features via GitHub Issues
- **Discussions**: Join community discussions for general questions
- **Documentation**: Check the `/docs` folder for detailed guides
- **Examples**: See `/examples` for usage patterns and tutorials

---

**Built with basketball passion and AI innovation** 🏀🤖

*Leveraging AgentOS, MLflow, and modern Python tooling to revolutionize basketball analytics.*
A powerful multi-agent orchestration platform built with the [Agno framework](https://docs.agno.com/) that enables seamless coordination between AI agents to analyze basketball statistic
