from alibi_detect import KSDrift
import numpy as np
from google.cloud import storage

def detect_drift(bucket_name, reference_path, current_data):
    """
    Detect data drift using Kolmogorov-Smirnov test
    """
    # Load reference data from GCS
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(reference_path)
    reference_data = np.load(blob.download_as_string())
    
    # Initialize drift detector
    drift_detector = KSDrift(
        p_val=0.05,
        X_ref=reference_data
    )
    
    # Check for drift
    preds = drift_detector.predict(current_data)
    
    return {
        'drift_detected': preds['data']['is_drift'],
        'p_value': float(preds['data']['p_val']),
        'threshold': 0.05
    }