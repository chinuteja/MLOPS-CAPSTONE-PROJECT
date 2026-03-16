# ---------------------------------------------------------
# IMPORTS
# ---------------------------------------------------------

import os
import pickle
from dotenv import load_dotenv

import mlflow
import mlflow.sklearn
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

# ---------------------------------------------------------
# AUTHENTICATION FOR DAGSHUB MLFLOW
# ---------------------------------------------------------

os.environ["MLFLOW_TRACKING_USERNAME"] = dagshub_token
os.environ["MLFLOW_TRACKING_PASSWORD"] = dagshub_token

mlflow.set_tracking_uri(
    f"https://dagshub.com/{repo_owner}/{repo_name}.mlflow"
)

mlflow.set_experiment("my-dvc-pipeline")


# ---------------------------------------------------------
# LOAD MODEL
# ---------------------------------------------------------

with open("models/model.pkl", "rb") as f:
    model = pickle.load(f)


# ---------------------------------------------------------
# REGISTER MODEL
# ---------------------------------------------------------

with mlflow.start_run():

    model_info = mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="model",
        registered_model_name="my_model_new"
    )

    client = MlflowClient()

    model_version = model_info.registered_model_version

    client.transition_model_version_stage(
        name="my_model_new",
        version=model_version,
        stage="Staging",
        archive_existing_versions=False
    )

    client.set_model_version_tag(
        name="my_model_new",
        version=model_version,
        key="type",
        value="staging"
    )

    print(f"Model version {model_version} transitioned to Staging.")