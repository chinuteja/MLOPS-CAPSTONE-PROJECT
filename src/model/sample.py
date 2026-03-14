import mlflow
import mlflow.sklearn
import pickle
import dagshub

repo_owner = "chinuteja2008"
repo_name = "MLOPS-CAPSTONE-PROJECT"

# Initialize Dagshub
dagshub.init(repo_owner=repo_owner, repo_name=repo_name, mlflow=True)

# Set tracking URI
mlflow.set_tracking_uri(
    f"https://dagshub.com/{repo_owner}/{repo_name}.mlflow"
)

run_id = "73d71f6cf8cc4d72b96ec9b20127eb47"

# Load local model
with open("models/model.pkl", "rb") as f:
    model = pickle.load(f)

# Attach to existing run
with mlflow.start_run(run_id=run_id):

    mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="model"
    )

print("Model successfully logged to MLflow run")