'''
This module defines an agent configured to interact with a MS SQL Server instance via MCPTools.
'''
from textwrap import dedent
import pandas_toon
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union, cast

from agno.tools import tool
from agno.agent import Agent
from agno.tools.reasoning import ReasoningTools
from agno.tools.workflow import WorkflowTools

from workflow.generate_game_report import game_report_workflow

from utils.agent_instructions import get_report_agent_instructions
from utils.logger import get_logger
from utils.config import (
    get_llm_config,
    sqlite_db,
    llm_catalog,
    )

# Initialize logger
logger = get_logger()

# Add example for agent running workflow
FEW_SHOT_EXAMPLES = dedent("""\
    You can refer to the examples below as guidance for how to use each tool.
    ### Examples
    #### Example: Game Report Workflow
    User: Please create a report for the game on December 1st, 2025, Houston Rockets versus Utah Jazz.
    Run: additional_data={"date": date, "home_team": home_team}
    
    You HAVE TO USE additional_data to pass the topic and style to the workflow.
""")

workflow_tools = WorkflowTools(
    workflow=game_report_workflow,
    add_few_shot=True,  # Include built-in examples
    few_shot_examples=FEW_SHOT_EXAMPLES,
    async_mode=False
)

def create_agent(llm: str, llm_reasoning: Optional[str]) -> Agent:
    '''
    This function creates an agent as basketball analyst.

    Args:
        llm: The LLM model to use for the team ("claude", "OpenAI-mini","OpenAI" or "AzureOpenAI")
        model_id: The model ID to use for the LLM. Options: "claude-sonnet-4-5", "gpt-4.1-mini", "gpt-4.1"
    '''

    agent = Agent(
        name="Basketball Game Report Agent",
        model=get_llm_config(
                    provider=llm,
                    model_id=llm_catalog.get(llm)
                    ),
        db=sqlite_db(),
        tools=[
            workflow_tools,
            ],
        instructions=get_report_agent_instructions(),
        add_history_to_context=True,
        enable_user_memories=True,
        markdown=True,
    )

    return agent