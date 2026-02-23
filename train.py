import os
import pandas as pd
import mlflow
import mlflow.sklearn
from mlflow.models import infer_signature
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split

def ingest_data() -> tuple:
    data = fetch_california_housing()
    x = pd.DataFrame(data.data, columns=data.feature_names)
    y = data.target
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state=36)
    print("Done ingesting data!")
    return X_train, X_test, y_train,y_test

def execute_continuous_training(X_train, X_test, y_train, y_test):
    MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI")

    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment("Manual_MLOps_CH")

    with mlflow.start_run():
        mlflow.log_param("max_depth", 100)
        mlflow.log_param("criterion", "friedman_mse")
        model = DecisionTreeRegressor(max_depth = 100, criterion = "friedman_mse", random_state=36)
        model.fit(X_train, y_train)

        prediction = model.predict(X_test)
        mean = mean_absolute_error(y_test, prediction)
        r2 = r2_score(y_test, prediction)
        mlflow.log_metric("mae", mean)
        mlflow.log_metric("r2", r2)
        if r2 > 0.5:
            signature = infer_signature(X_test, y_test)
            mlflow.sklearn.log_model(model, artifact_path = "models", signature = signature, registered_model_name = "DTRegressor")
            print("Done!")
        else:
            print( "Nope! Train again.")

if __name__ == "__main__":
    X_train, X_test, y_train,y_test = ingest_data()
    execute_continuous_training(X_train, X_test, y_train,y_test)
