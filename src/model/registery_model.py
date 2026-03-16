import pickle
import mlflow
import mlflow.sklearn
import dagshub
import os
from mlflow.tracking import MlflowClient
from dotenv import load_dotenv
load_dotenv()

repo_owner = os.getenv("repo_owner")
repo_name = os.getenv("repo_name")

dagshub.init(repo_owner=repo_owner, repo_name=repo_name, mlflow=True)

mlflow.set_tracking_uri(
    f"https://dagshub.com/{repo_owner}/{repo_name}.mlflow"
)

mlflow.set_experiment("my-dvc-pipeline")

# load local model
with open("models/model.pkl", "rb") as f:
    model = pickle.load(f)

# create a new MLflow run
# 1. Start the run
with mlflow.start_run() as run:
    
    # 2. Log and Register the model
    # This creates a new version of "my_model_new"
    model_info = mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="model",
        registered_model_name="my_model_new"
    )

    # 3. Use the Client to transition the version to a Stage
    client = MlflowClient()
    
    # Get the version number that was just created
    model_version = model_info.registered_model_version
    
    client.transition_model_version_stage(
        name="my_model_new",
        version=model_version,
        stage="Staging",  # Fixed the typo here
        archive_existing_versions=False
    )
    
    # 4. Set tags on the model version (if needed)
    client.set_model_version_tag(
        name="my_model_new",
        version=model_version,
        key="type",
        value="staging"
    )

    print(f"Model version {model_version} transitioned to Staging.")
