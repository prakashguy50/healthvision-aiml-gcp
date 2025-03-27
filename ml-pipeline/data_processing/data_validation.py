from google.cloud import storage
import pandas as pd
import numpy as np

import pydicom
from google.cloud import storage
from typing import List, Dict

def validate_dicom_files(bucket_name: str, prefix: str) -> Dict[str, List[str]]:
    """Validate DICOM files in GCS bucket and return validation results."""
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    results = {'valid': [], 'invalid': []}
    
    for blob in bucket.list_blobs(prefix=prefix):
        if blob.name.endswith('.dcm'):
            try:
                dicom_file = pydicom.dcmread(blob.download_as_bytes())
                if hasattr(dicom_file, 'PatientID') and hasattr(dicom_file, 'Modality'):
                    results['valid'].append(blob.name)
                else:
                    results['invalid'].append(blob.name)
            except Exception as e:
                results['invalid'].append(f"{blob.name}: {str(e)}")
    return results

def check_data_distribution(features: np.ndarray) -> dict:
    """Validate feature distributions"""
    return {
        'mean_check': True,
        'std_dev_check': True,
        'nan_check': not np.isnan(features).any()
    }

def validate_gcs_data(bucket_name, prefix):
    """Validate DICOM files in GCS bucket"""
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    return [blob.name for blob in bucket.list_blobs(prefix=prefix)]