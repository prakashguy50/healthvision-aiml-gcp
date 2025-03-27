#!/bin/bash

# Deploy model to Vertex AI
gcloud ai models upload \
  --region=us-central1 \
  --display-name=ultrasound-model \
  --container-image-uri=us-docker.pkg.dev/vertex-ai/prediction/tf2-cpu.2-6:latest \
  --artifact-uri=gs://$1/models/ultrasound/

# Create endpoint
gcloud ai endpoints create \
  --region=us-central1 \
  --display-name=ultrasound-endpoint

# Deploy model to endpoint
ENDPOINT_ID=$(gcloud ai endpoints list --region=us-central1 --format="value(ENDPOINT_ID)" --filter="displayName=ultrasound-endpoint")
MODEL_ID=$(gcloud ai models list --region=us-central1 --format="value(MODEL_ID)" --filter="displayName=ultrasound-model")

gcloud ai endpoints deploy-model $ENDPOINT_ID \
  --region=us-central1 \
  --model=$MODEL_ID \
  --display-name=ultrasound-deployment \
  --machine-type=n1-standard-4 \
  --min-replica-count=1 \
  --max-replica-count=3