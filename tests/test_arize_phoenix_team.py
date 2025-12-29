import os
import asyncio

from agno.agent import Agent
from agno.team import Team
from agno.models.openai import OpenAIChat
from agno.tools.python import PythonTools
from agno.tools.local_file_system import LocalFileSystemTools

from openinference.instrumentation.agno import AgnoInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk import trace as trace_sdk
from opentelemetry import trace as trace_api
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

from dotenv import load_dotenv
load_dotenv()

endpoint = "http://127.0.0.1:6006/v1/traces"
tracer_provider = trace_sdk.TracerProvider()
tracer_provider.add_span_processor(SimpleSpanProcessor(OTLPSpanExporter(endpoint)))
# Optionally, you can also print the spans to the console.
tracer_provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))

trace_api.set_tracer_provider(tracer_provider=tracer_provider)

# Start instrumenting agno
AgnoInstrumentor().instrument()

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
        #stream=True
        )
    )