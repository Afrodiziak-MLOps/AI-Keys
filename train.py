import mlflow
import random
import datetime

MLFLOW_TRACKING_URI = "http://localhost:5001"
EXPERIMENT_NAME = "CI_CD_Training"

def train_model(learning_rate, batch_size, model_type):
    """Имитирует обучение модели и возвращает метрики."""
    accuracy = round(random.uniform(0.75, 0.99), 4)
    loss = round(random.uniform(0.05, 0.5), 4)
    return accuracy, loss

def main():
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment(EXPERIMENT_NAME)

    params = [
        {"lr": 0.001, "batch": 32, "model": "RandomForest"},
        {"lr": 0.01, "batch": 64, "model": "XGBoost"},
        {"lr": 0.1, "batch": 128, "model": "LightGBM"},
    ]

    best_accuracy = 0
    best_run_id = None

    for i, p in enumerate(params, 1):
        with mlflow.start_run(run_name=f"Train_{i}_{p['model']}"):
            mlflow.log_param("learning_rate", p["lr"])
            mlflow.log_param("batch_size", p["batch"])
            mlflow.log_param("model_type", p["model"])

            accuracy, loss = train_model(p["lr"], p["batch"], p["model"])

            mlflow.log_metric("accuracy", accuracy)
            mlflow.log_metric("loss", loss)

            print(f"✅ Run {i}: Model={p['model']}, Accuracy={accuracy}, Loss={loss}")

            if accuracy > best_accuracy:
                best_accuracy = accuracy
                best_run_id = mlflow.active_run().info.run_id

    print(f"\n🏆 Best model: {best_run_id} (Accuracy: {best_accuracy})")

    with open("training_results.txt", "w") as f:
        f.write(f"Best accuracy: {best_accuracy}\n")
        f.write(f"Best run ID: {best_run_id}\n")
        f.write(f"Timestamp: {datetime.datetime.now()}\n")

    print("📄 Results saved to training_results.txt")

if __name__ == "__main__":
    main()
