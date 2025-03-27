import numpy as np
import pydicom
from google.cloud import storage


def extract_dicom_features(bucket_name: str, file_path: str) -> dict:
    """Extract features from DICOM file in GCS."""
    client = storage.Client()
    blob = client.bucket(bucket_name).blob(file_path)
    dicom = pydicom.dcmread(blob.download_as_bytes())
    
    features = {
        'patient_id': getattr(dicom, 'PatientID', ''),
        'modality': getattr(dicom, 'Modality', ''),
        'rows': getattr(dicom, 'Rows', 0),
        'columns': getattr(dicom, 'Columns', 0),
        'pixel_spacing': getattr(dicom, 'PixelSpacing', [1.0, 1.0]),
        'pixel_data_stats': {
            'mean': np.mean(dicom.pixel_array) if hasattr(dicom, 'pixel_array') else 0,
            'std': np.std(dicom.pixel_array) if hasattr(dicom, 'pixel_array') else 0
        }
    }
    return features

def upload_features_to_gcs(features, bucket_name, destination_path):
    """Upload processed features to GCS"""
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_path)
    
    blob.upload_from_string(str(features))
    
    return f"gs://{bucket_name}/{destination_path}"