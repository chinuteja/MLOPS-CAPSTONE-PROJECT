# ---------------------------------------------------------
# IMPORTS
# ---------------------------------------------------------

import os
import pickle
from dotenv import load_dotenv

import mlflow
import mlflow.sklearn
import dagshub
from mlflow.tracking import MlflowClient


# ---------------------------------------------------------
# LOAD ENV VARIABLES
# ---------------------------------------------------------

load_dotenv()

repo_owner = os.getenv("repo_owner")
repo_name = os.getenv("repo_name")
dagshub_token = os.getenv("CAPSTONE_TEST")

if not dagshub_token:
    raise EnvironmentError("CAPSTONE_TEST environment variable is not set")

# Set authentication for DagsHub MLflow
os.environ["MLFLOW_TRACKING_USERNAME"] = dagshub_token
os.environ["MLFLOW_TRACKING_PASSWORD"] = dagshub_token


# ---------------------------------------------------------
# DAGSHUB + MLFLOW SETUP
# ---------------------------------------------------------

dagshub.init(repo_owner=repo_owner, repo_name=repo_name, mlflow=True)

mlflow.set_tracking_uri(
    f"https://dagshub.com/{repo_owner}/{repo_name}.mlflow"
)

mlflow.set_experiment("my-dvc-pipeline")


# ---------------------------------------------------------
# LOAD TRAINED MODEL
# ---------------------------------------------------------

with open("models/model.pkl", "rb") as f:
    model = pickle.load(f)


# ---------------------------------------------------------
# MODEL REGISTRATION PIPELINE
# ---------------------------------------------------------

with mlflow.start_run() as run:

    # Log model and register it
    model_info = mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="model",
        registered_model_name="my_model_new"
    )

    # Create MLflow client
    client = MlflowClient()

    # Get model version created during registration
    model_version = model_info.registered_model_version

    # Move model to Staging
    client.transition_model_version_stage(
        name="my_model_new",
        version=model_version,
        stage="Staging",
        archive_existing_versions=False
    )

    # Add tag to the model version
    client.set_model_version_tag(
        name="my_model_new",
        version=model_version,
        key="type",
        value="staging"
    )

    print(f"Model version {model_version} transitioned to Staging.")