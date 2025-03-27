from google.cloud import monitoring_v3
import time

def log_metrics(project_id, model_id, metrics):
    """
    Log model performance metrics to Cloud Monitoring
    """
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"
    
    series = monitoring_v3.TimeSeries()
    series.resource.type = "generic_task"
    series.resource.labels["project_id"] = project_id
    series.resource.labels["location"] = "global"
    series.resource.labels["namespace"] = "healthvision"
    series.resource.labels["job"] = f"ml-model-{model_id}"
    
    now = time.time()
    seconds = int(now)
    nanos = int((now - seconds) * 10**9)
    
    for metric_name, metric_value in metrics.items():
        point = monitoring_v3.Point({
            "interval": {
                "end_time": {
                    "seconds": seconds,
                    "nanos": nanos
                }
            },
            "value": {
                "double_value": metric_value
            }
        })
        
        series.metric.type = f"custom.googleapis.com/ml_models/{metric_name}"
        series.points = [point]
        client.create_time_series(name=project_name, time_series=[series])