'''
This module defines a workflow to generate game reports for NBA games using Agno's workflow and agent capabilities.
'''
import pandas as pd
import pandas_toon

from agno.workflow import Step, Workflow, StepInput, StepOutput
from agno.agent import Agent

import sys
import os
# Add src to path to import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from utils.logger import get_logger
from utils.mlflow_tracer import setup_mlflow_tracer
from utils.config import (
    llm,
    get_llm_config,
    sqlite_db,
    llm_catalog,
    MLFLOW_TRACING,
    MLFLOW_TRACK_SERVER,
    MLFLOW_EXPERIMENT_NAME,
    DATABRICKS_HOST,
    )

import typer
app = typer.Typer()

# Initialize logger
logger = get_logger()

def get_input_message(date: str, home_team: str, away_team: str):
    '''
    Create input message for the workflow based on the parameters.
    '''
    message = f'''
        Create a report of the game between {away_team} and the home team {home_team} on {date}.
        Create this report based on the play be play statistic retrieved from the data source.
        Describe the game like a game report in the newspaper.
        Include the following information in the report:
        
        - Game summary
        - Game highlights
        - Game statistics

        Format the response using markdown and include tables where appropriate.
        '''
    
    return message

def read_game_stats(step_input: StepInput):
    '''
    This function reads the game statistics from Basketball Reference.
    '''

    try: 
        input_message = step_input.input
        date = step_input.additional_data.get("date")
        home_team = step_input.additional_data.get("home_team")
     
        url=f"https://www.basketball-reference.com/boxscores/pbp/{date}0{home_team}.html"

        df = pd.read_html(url)[0].droplevel(0, axis=1)

        logger.info(f"Successfully fetched game stats from {url}")
    
    except Exception as e:
        logger.error(f"Error fetching game stats: {e}")

    return StepOutput(content=df.to_toon())

def get_report_agent() -> Agent:
    '''
    Define the agent responsible for generating game reports.
    '''

    agent = Agent(
                model=get_llm_config(
                    provider=llm,
                    model_id=llm_catalog.get(llm)
                    ),
                description='''You are an expert in generating game report for NBA games.''',
                instructions=['''
                          Describe the game like a game report in the newspaper.
                          The data needed for the report will be provided from the previous step.
                          '''],
                )
    return agent

# Define workflow

def game_report_workflow():
    '''
    Define the workflow to generate game reports.
    '''
    report_agent = get_report_agent()

    workflow = Workflow(
        name="Create Game Report",
        steps=[
            Step(name="Search Phase", executor=read_game_stats),
            Step(name="Writing Phase", agent=report_agent),
        ]
    )

    return workflow

@app.command()
def main(
    date: str = typer.Option(
        "20251116", 
        help="Date of the game."
        ),
    home_team: str = typer.Option(
        "HOU", 
        help="Abbreviation of the home team (e.g., LAL for Los Angeles Lakers)."
        ),
    away_team: str = typer.Option(
        "ORL", 
        help="Abbreviation of the away team (e.g., BOS for Boston Celtics)."
        )
):
    '''
    Entry point for typer app command.
    '''
    
    input_message = get_input_message(date, home_team, away_team)

    workflow = game_report_workflow()

    workflow.print_response(
        input=input_message,
        additional_data={"date": date, "home_team": home_team},
        markdown=True
        )

if __name__ == "__main__":
    # Set NO_PROXY to avoid proxy for localhost connections
    os.environ["NO_PROXY"] = "localhost, 127.0.0.1"
    os.environ["no_proxy"] = "localhost, 127.0.0.1"

    # Set up mlflow tracer
    if MLFLOW_TRACING == 'true':
        setup_mlflow_tracer(
            track_server=MLFLOW_TRACK_SERVER,
            experiment_name=MLFLOW_EXPERIMENT_NAME
                        )
        if MLFLOW_TRACK_SERVER == "databricks":
            logger.info(f"Initialized mlflow trace to Databricks: {DATABRICKS_HOST}")
        else:
            logger.info("Initialized mlflow trace to http://localhost:5000")
    
    # Run Typer App 
    app()