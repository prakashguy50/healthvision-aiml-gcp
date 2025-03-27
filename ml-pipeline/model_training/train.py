import argparse
import tensorflow as tf
from google.cloud import aiplatform, storage
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_data_from_gcs(bucket_name: str, prefix: str) -> tuple:
    """Load and preprocess data from GCS bucket"""
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blobs = list(bucket.list_blobs(prefix=prefix))
    
    if not blobs:
        raise ValueError(f"No files found in gs://{bucket_name}/{prefix}")
    
    # Implement actual data loading logic
    features, labels = [], []
    for blob in blobs:
        if blob.name.endswith('.npy'):
            data = np.load(blob.download_as_bytes())
            features.append(data['features'])
            labels.append(data['label'])
    
    return np.array(features), np.array(labels)

def build_model(input_shape: tuple, num_classes: int) -> tf.keras.Model:
    """Build and compile TensorFlow model"""
    model = tf.keras.Sequential([
        tf.keras.layers.InputLayer(input_shape=input_shape),
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(num_classes, activation='softmax')
    ])
    
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    return model

def train_and_deploy(args):
    """Main training and deployment function"""
    aiplatform.init(project=args.project, location=args.region)
    
    # Load data
    X, y = load_data_from_gcs(args.bucket, args.data_prefix)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    
    # Build and train model
    model = build_model(input_shape=X_train[0].shape, num_classes=len(np.unique(y)))
    model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=args.epochs)
    
    # Save model
    model.save(args.model_dir)
    
    # Deploy to Vertex AI if requested
    if args.deploy:
        deployed_model = aiplatform.Model.upload(
            display_name=args.model_name,
            artifact_uri=f"gs://{args.bucket}/{args.model_gcs_path}",
            serving_container_image_uri=args.serving_image
        )
        endpoint = deployed_model.deploy(
            machine_type=args.machine_type,
            min_replica_count=1,
            max_replica_count=3
        )
        logger.info(f"Model deployed to endpoint: {endpoint.resource_name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True, help="GCP project ID")
    parser.add_argument("--region", default="us-central1", help="GCP region")
    parser.add_argument("--bucket", required=True, help="GCS bucket name")
    parser.add_argument("--data_prefix", default="data/processed", help="GCS data prefix")
    parser.add_argument("--model_dir", default="/tmp/model", help="Local model directory")
    parser.add_argument("--model_gcs_path", default="models/ultrasound", help="GCS model path")
    parser.add_argument("--model_name", default="ultrasound-classifier", help="Model display name")
    parser.add_argument("--epochs", type=int, default=10, help="Training epochs")
    parser.add_argument("--deploy", action="store_true", help="Deploy to Vertex AI")
    parser.add_argument("--serving_image", 
                      default="us-docker.pkg.dev/vertex-ai/prediction/tf2-cpu.2-12:latest",
                      help="Serving container image")
    parser.add_argument("--machine_type", default="n1-standard-4", help="Deployment machine type")
    
    args = parser.parse_args()
    train_and_deploy(args)