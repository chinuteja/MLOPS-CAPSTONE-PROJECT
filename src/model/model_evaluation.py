import numpy as np
import pandas as pd
import pickle
import json
import warnings
import os
from dotenv import load_dotenv

from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score

import mlflow
import mlflow.sklearn

from src.logger import logging

warnings.filterwarnings("ignore")

# ---------------------------------------------------------
# LOAD ENV VARIABLES
# ---------------------------------------------------------

load_dotenv()

repo_owner = os.getenv("repo_owner")
repo_name = os.getenv("repo_name")
dagshub_token = os.getenv("CAPSTONE_TEST")

# ---------------------------------------------------------
# DAGSHUB + MLFLOW SETUP
# ---------------------------------------------------------

if dagshub_token:
    os.environ["MLFLOW_TRACKING_USERNAME"] = dagshub_token
    os.environ["MLFLOW_TRACKING_PASSWORD"] = dagshub_token

try:
    import dagshub
    dagshub.init(
        repo_owner=repo_owner,
        repo_name=repo_name,
        mlflow=True
    )
except Exception:
    print("Skipping Dagshub initialization in CI")

mlflow.set_tracking_uri(
    f"https://dagshub.com/{repo_owner}/{repo_name}.mlflow"
)

mlflow.set_experiment("my-dvc-pipeline")

# ---------------------------------------------------------
# FUNCTIONS
# ---------------------------------------------------------


def load_model(file_path: str):
    """Load trained model"""
    try:
        with open(file_path, "rb") as file:
            model = pickle.load(file)

        logging.info(f"Model loaded successfully from {file_path}")
        return model

    except Exception as e:
        logging.error(f"Error loading model: {e}")
        raise


def load_data(file_path: str) -> pd.DataFrame:
    """Load dataset"""
    try:
        df = pd.read_csv(file_path)

        logging.info(f"Data loaded successfully from {file_path}")
        return df

    except Exception as e:
        logging.error(f"Error loading data: {e}")
        raise


def evaluate_model(model, X_test, y_test):
    """Evaluate model performance"""

    try:

        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1]

        metrics = {
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred),
            "recall": recall_score(y_test, y_pred),
            "auc": roc_auc_score(y_test, y_pred_proba)
        }

        logging.info("Model evaluation completed")

        return metrics

    except Exception as e:
        logging.error(f"Error evaluating model: {e}")
        raise


def save_metrics(metrics: dict, path: str):
    """Save metrics to JSON"""

    try:

        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, "w") as f:
            json.dump(metrics, f, indent=4)

        logging.info(f"Metrics saved to {path}")

    except Exception as e:
        logging.error(f"Error saving metrics: {e}")
        raise


def save_model_info(run_id: str, artifact_path: str, path: str):
    """Save experiment run information"""

    try:

        os.makedirs(os.path.dirname(path), exist_ok=True)

        model_info = {
            "run_id": run_id,
            "model_path": artifact_path
        }

        with open(path, "w") as f:
            json.dump(model_info, f, indent=4)

        logging.info("Experiment info saved")

    except Exception as e:
        logging.error(f"Error saving experiment info: {e}")
        raise


# ---------------------------------------------------------
# MAIN PIPELINE
# ---------------------------------------------------------


def main():

    with mlflow.start_run() as run:

        try:

            # -----------------------------------------------
            # LOAD MODEL + DATA
            # -----------------------------------------------

            model = load_model("models/model.pkl")

            test_df = load_data("data/processed/test_bow.csv")

            X_test = test_df.iloc[:, :-1]
            y_test = test_df.iloc[:, -1]

            # -----------------------------------------------
            # MODEL EVALUATION
            # -----------------------------------------------

            metrics = evaluate_model(model, X_test, y_test)

            # -----------------------------------------------
            # SAVE METRICS LOCALLY
            # -----------------------------------------------

            save_metrics(metrics, "reports/metrics.json")

            # -----------------------------------------------
            # LOG METRICS TO MLFLOW
            # -----------------------------------------------

            mlflow.log_metrics(metrics)

            # -----------------------------------------------
            # LOG MODEL PARAMETERS
            # -----------------------------------------------

            if hasattr(model, "get_params"):

                params = model.get_params()

                for key, value in params.items():
                    mlflow.log_param(key, value)

            # -----------------------------------------------
            # LOG MODEL
            # -----------------------------------------------

            mlflow.sklearn.log_model(
                sk_model=model,
                artifact_path="model"
            )

            logging.info("Model logged to MLflow")

            # -----------------------------------------------
            # SAVE RUN INFO
            # -----------------------------------------------

            save_model_info(
                run.info.run_id,
                "model",
                "reports/experiment_info.json"
            )

            # -----------------------------------------------
            # LOG METRICS FILE AS ARTIFACT
            # -----------------------------------------------

            mlflow.log_artifact("reports/metrics.json")

            print("Metrics:", metrics)

        except Exception as e:

            logging.error(f"Pipeline failed: {e}")
            print(f"Error: {e}")


# ---------------------------------------------------------

if __name__ == "__main__":
    main()