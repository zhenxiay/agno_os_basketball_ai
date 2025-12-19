'''
This is a test script to reproduce the MLflow issue with Team agents in Agno OS.
'''
import os
import asyncio
from dotenv import load_dotenv
import mlflow
from agno.agent import Agent
from agno.team import Team
from agno.models.openai import OpenAIChat
from agno.tools.python import PythonTools
from agno.tools.local_file_system import LocalFileSystemTools

# Load api-key from .env file
load_dotenv()

# Setup
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("test-experiment")

# Enable Agno autolog
mlflow.agno.autolog()

# Create agents
python_agent = Agent(
    name="Python Agent",
    model=OpenAIChat(id="gpt-4.1"),
    instructions="You are an expert in python programming ."
)

file_agent = Agent(
    name="File Agent",
    instructions=["You are a file management assistant that helps save content to local files"],
    model=OpenAIChat(id="gpt-4.1"),
    tools=[LocalFileSystemTools(target_directory="./output")],
)

# Create Team
team= Team(
    name="Test Team",
    model=OpenAIChat(id="gpt-4.1"),
    instructions="You are the team leader who coordinates the task execution with your members.",
    members=[python_agent, file_agent],
    share_member_interactions=True,
    markdown=True,
)

if __name__ == "__main__":

    # Set NO_PROXY to avoid proxy for localhost connections
    os.environ["NO_PROXY"] = "localhost, 127.0.0.1"
    os.environ["no_proxy"] = "localhost, 127.0.0.1"

    asyncio.run(team.aprint_response(
        "Write a python script which prints Hello World and save it to a local folder.",
        stream=True
        )
    )