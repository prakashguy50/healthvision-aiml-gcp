import numpy as np
import pydicom
from google.cloud import storage

def extract_dicom_features(dicom_file):
    """Extract features from DICOM file"""
    ds = pydicom.dcmread(dicom_file)
    
    features = {
        'pixel_array_shape': ds.pixel_array.shape,
        'modality': ds.Modality,
        'bits_stored': ds.BitsStored,
        # Add more DICOM metadata as needed
    }
    
    if hasattr(ds, 'PixelData'):
        pixel_data = ds.pixel_array
        features.update({
            'mean_intensity': np.mean(pixel_data),
            'max_intensity': np.max(pixel_data)
        })
    
    return features

def upload_features_to_gcs(features, bucket_name, destination_path):
    """Upload processed features to GCS"""
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_path)
    
    blob.upload_from_string(str(features))
    
    return f"gs://{bucket_name}/{destination_path}"