import mlflow
import random
import datetime
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

MLFLOW_TRACKING_URI = os.environ.get("MLFLOW_TRACKING_URI", "http://localhost:5001")
EXPERIMENT_NAME = "CI_CD_Training"

def train_real_model():
    """Обучает реальную модель на Iris dataset."""
    iris = load_iris()
    X_train, X_test, y_train, y_test = train_test_split(
        iris.data, iris.target, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    return model, accuracy

def main():
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment(EXPERIMENT_NAME)

    with mlflow.start_run(run_name=f"Train_Iris_{datetime.datetime.now().strftime('%H%M%S')}"):
        model, accuracy = train_real_model()

        mlflow.log_param("model_type", "RandomForest")
        mlflow.log_param("n_estimators", 100)
        mlflow.log_metric("accuracy", accuracy)

        # Сохраняем модель в MLflow
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="model",
            registered_model_name="IrisClassifier"
        )

        print(f"✅ Model trained! Accuracy: {accuracy:.4f}")

        # Записываем результаты
        with open("training_results.txt", "w") as f:
            f.write(f"Best accuracy: {accuracy}\n")
            f.write(f"Model: IrisClassifier\n")
            f.write(f"Timestamp: {datetime.datetime.now()}\n")

if __name__ == "__main__":
    main()
