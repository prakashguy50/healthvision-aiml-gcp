#!/bin/bash
# Deploy model to Vertex AI
PROJECT=$1
MODEL_DIR=$2

gcloud ai models upload \
  --project=$PROJECT \
  --region=us-central1 \
  --display-name=healthvision-model \
  --container-image-uri=us-docker.pkg.dev/vertex-ai/prediction/tf2-cpu.2-12:latest \
  --artifact-uri=$MODEL_DIR

gcloud ai endpoints create \
  --project=$PROJECT \
  --region=us-central1 \
  --display-name=healthvision-endpoint

ENDPOINT_ID=$(gcloud ai endpoints list --region=us-central1 --format="value(ENDPOINT_ID)")
MODEL_ID=$(gcloud ai models list --region=us-central1 --format="value(MODEL_ID)")

gcloud ai endpoints deploy-model $ENDPOINT_ID \
  --project=$PROJECT \
  --region=us-central1 \
  --model=$MODEL_ID \
  --display-name=prod-deployment \
  --machine-type=n1-standard-4 \
  --min-replica-count=1 \
  --max-replica-count=3 \
  --traffic-split=0=100