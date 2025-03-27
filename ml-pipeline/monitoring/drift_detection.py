from google.cloud import bigquery, monitoring_v3
import numpy as np
from scipy import stats
import argparse

def detect_drift(project_id: str, dataset_id: str, table_id: str, feature_column: str):
    """Detect data drift using Kolmogorov-Smirnov test"""
    client = bigquery.Client(project=project_id)
    
    # Get reference and current distributions
    query = f"""
    SELECT 
        {feature_column},
        COUNT(*) as count
    FROM `{project_id}.{dataset_id}.{table_id}`
    WHERE partition_date BETWEEN 
        DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY) AND CURRENT_DATE()
    GROUP BY 1
    """
    result = client.query(query).to_dataframe()
    
    # Calculate drift score (KS test)
    drift_score = stats.ks_2samp(
        result[feature_column].values,
        result[feature_column].sample(frac=0.5).values  # Simulated current data
    ).statistic
    
    # Alert if drift detected
    if drift_score > 0.2:
        alert_client = monitoring_v3.AlertPolicyServiceClient()
        policy = {
            "display_name": "Data Drift Alert",
            "conditions": [{
                "condition_threshold": {
                    "filter": f"metric.type=\"custom.googleapis.com/ml/drift_score\"",
                    "comparison": "COMPARISON_GT",
                    "threshold_value": 0.2,
                    "duration": "300s"
                }
            }]
        }
        alert_client.create_alert_policy(name=f"projects/{project_id}", alert_policy=policy)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_id", required=True)
    parser.add_argument("--dataset_id", required=True)
    parser.add_argument("--table_id", required=True)
    parser.add_argument("--feature_column", required=True)
    args = parser.parse_args()
    
    detect_drift(args.project_id, args.dataset_id, args.table_id, args.feature_column)