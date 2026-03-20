# ---------------------------------------------------------
# IMPORTS
# ---------------------------------------------------------

import os
import pickle
from dotenv import load_dotenv

import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient
import dagshub


# ---------------------------------------------------------
# LOAD ENV VARIABLES
# ---------------------------------------------------------

load_dotenv()


dagshub_token = os.getenv("CAPSTONE_TEST")
repo_owner = os.getenv("repo_owner")
repo_name = os.getenv("repo_name")
dagshub_url = "https://dagshub.com"
if not dagshub_token:
    raise EnvironmentError("CAPSTONE_TEST environment variable is not set")

os.environ["MLFLOW_TRACKING_USERNAME"] = dagshub_token
os.environ["MLFLOW_TRACKING_PASSWORD"] = dagshub_token

tracking_uri = f"{dagshub_url}/{repo_owner}/{repo_name}.mlflow"
os.environ["MLFLOW_REGISTRY_URI"] = tracking_uri
# Set up MLflow tracking URI
mlflow.set_tracking_uri(f'{dagshub_url}/{repo_owner}/{repo_name}.mlflow')



#comment for production, uncomment for local testing
# repo_owner = "chinuteja2008"
# repo_name = "MLOPS-CAPSTONE-PROJECT"
# #comment for local testing, uncomment for production
# dagshub.init(repo_owner=repo_owner, repo_name=repo_name, mlflow=True)
# mlflow.set_tracking_uri(
#     f"https://dagshub.com/{repo_owner}/{repo_name}.mlflow"
# )

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