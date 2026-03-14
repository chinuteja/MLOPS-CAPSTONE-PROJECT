import pickle
import mlflow
import mlflow.sklearn
import dagshub
import os
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
with mlflow.start_run() as run:

    mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="model",
        registered_model_name="my_model_new"
    )

    print("Run ID:", run.info.run_id)
    print("Model logged and registered successfully")