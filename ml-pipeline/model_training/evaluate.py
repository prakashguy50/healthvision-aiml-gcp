import tensorflow as tf
from google.cloud import aiplatform, monitoring_v3
import numpy as np
import argparse

def log_metrics_to_cloud_monitoring(project_id: str, metrics: dict):
    """Log custom metrics to Cloud Monitoring"""
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"
    
    for metric_name, metric_value in metrics.items():
        series = monitoring_v3.TimeSeries()
        series.metric.type = f"custom.googleapis.com/ml/{metric_name}"
        series.resource.type = "global"
        
        point = monitoring_v3.Point()
        point.value.double_value = metric_value
        now = monitoring_v3.TimeInterval()
        now.end_time.seconds = int(time.time())
        point.interval = now
        
        series.points = [point]
        client.create_time_series(name=project_name, time_series=[series])

def evaluate_model(model_path: str, test_data: np.ndarray, test_labels: np.ndarray, project_id: str):
    """Evaluate model and log metrics"""
    model = tf.keras.models.load_model(model_path)
    loss, accuracy = model.evaluate(test_data, test_labels)
    
    metrics = {
        "accuracy": accuracy,
        "loss": loss,
        "inference_latency": calculate_latency(model, test_data[:10])
    }
    
    log_metrics_to_cloud_monitoring(project_id, metrics)
    return metrics

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_path", required=True)
    parser.add_argument("--test_data", required=True)
    parser.add_argument("--test_labels", required=True)
    parser.add_argument("--project_id", required=True)
    args = parser.parse_args()
    
    test_data = np.load(args.test_data)
    test_labels = np.load(args.test_labels)
    
    metrics = evaluate_model(args.model_path, test_data, test_labels, args.project_id)
    print("Evaluation Metrics:", metrics)