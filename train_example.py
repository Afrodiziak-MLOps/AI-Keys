import mlflow
import random

mlflow.set_tracking_uri("http://localhost:5001")
mlflow.set_experiment("My First Experiment")

# Создаём 5 запусков с разными параметрами
for i in range(1, 6):
    lr = round(random.uniform(0.001, 0.1), 4)
    batch = random.choice([16, 32, 64, 128])
    model_type = random.choice(["RandomForest", "XGBoost", "LightGBM"])
    
    with mlflow.start_run(run_name=f"Run {i}"):
        mlflow.log_param("learning_rate", lr)
        mlflow.log_param("batch_size", batch)
        mlflow.log_param("model_type", model_type)
        
        accuracy = round(random.uniform(0.75, 0.99), 4)
        loss = round(random.uniform(0.05, 0.5), 4)
        
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("loss", loss)
        
        print(f"✅ Run {i}: LR={lr}, Batch={batch}, Model={model_type}, Acc={accuracy}")

print("🎉 All experiments logged to MLflow!")