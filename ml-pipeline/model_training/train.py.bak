import argparse
import tensorflow as tf
from google.cloud import aiplatform, storage
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import pickle

def load_data_from_gcs(bucket_name, prefix):
    """Load DICOM metadata from GCS"""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    
    features = []
    labels = []
    
    for blob in bucket.list_blobs(prefix=prefix):
        if blob.name.endswith('.metadata'):
            content = blob.download_as_text()
            # Parse metadata and extract features/labels
            # ...
    
    return np.array(features), np.array(labels)

def build_model(input_shape, num_classes):
    """Build CNN model for ultrasound analysis"""
    model = tf.keras.Sequential([
        tf.keras.layers.InputLayer(input_shape=input_shape),
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(num_classes, activation='softmax')
    ])
    
    model.compile(optimizer='adam',
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])
    
    return model

def train_and_deploy(args):
    # Initialize Vertex AI
    aiplatform.init(project=args.project, location=args.region)
    
    # Load data
    X, y = load_data_from_gcs(args.bucket, args.data_prefix)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    
    # Build model
    model = build_model(input_shape=X_train[0].shape, num_classes=len(np.unique(y)))
    
    # Train
    model.fit(X_train, y_train, 
             validation_data=(X_test, y_test),
             epochs=args.epochs,
             batch_size=32)
    
    # Save model
    model.save(args.model_dir)
    
    # Upload to GCS
    if args.model_gcs_path:
        storage_client = storage.Client()
        bucket = storage_client.bucket(args.bucket)
        for file in tf.io.gfile.listdir(args.model_dir):
            local_path = tf.io.gfile.join(args.model_dir, file)
            blob = bucket.blob(f"{args.model_gcs_path}/{file}")
            blob.upload_from_filename(local_path)
    
    # Deploy to Vertex AI
    if args.deploy:
        deployed_model = aiplatform.Model.upload(
            display_name=args.model_name,
            artifact_uri=f"gs://{args.bucket}/{args.model_gcs_path}",
            serving_container_image_uri=args.serving_image)
        
        endpoint = deployed_model.deploy(
            machine_type=args.machine_type,
            min_replica_count=1,
            max_replica_count=3)
        
        print(f"Model deployed to: {endpoint.resource_name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--region", default="us-central1")
    parser.add_argument("--bucket", required=True)
    parser.add_argument("--data_prefix", default="data/processed")
    parser.add_argument("--model_dir", default="/tmp/model")
    parser.add_argument("--model_gcs_path", default="models/ultrasound")
    parser.add_argument("--model_name", default="ultrasound-classifier")
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--deploy", action="store_true")
    parser.add_argument("--serving_image", 
                       default="us-docker.pkg.dev/vertex-ai/prediction/tf2-cpu.2-6:latest")
    parser.add_argument("--machine_type", default="n1-standard-4")
    
    args = parser.parse_args()
    train_and_deploy(args)