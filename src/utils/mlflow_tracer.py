'''
This module sets up the agent run trace to MLflow.
'''
import mlflow

from utils.logger import get_logger
from utils.config import llm

# Initialize the logger
logger = get_logger()

def setup_mlflow_tracer(track_server: str, experiment_name: str) -> None:
    '''
    This function sets up MLflow to trace the agent runs.
    It configures the tracking URI to Databricks or to a local server and sets the experiment name,
    '''

    # Set tracking URI and experiment name based on the server type    
    if track_server == "databricks":
        mlflow.set_tracking_uri("databricks")
        mlflow.set_experiment(f"/{experiment_name}")
    else:
        mlflow.set_tracking_uri("http://localhost:5000")
        mlflow.set_experiment(experiment_name)
    
    if llm == "AzureOpenAI" or llm == "OpenAI":
        # Enable autologging for Azure OpenAI models
        mlflow.openai.autolog()
        logger.info("MLflow OpenAI autolog enabled.")
    else:
        mlflow.anthropic.autolog()
