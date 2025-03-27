#!/bin/bash
# Initialize GCP environment for HealthVision AI

PROJECT_ID=$1
REGION=${2:-us-central1}

# Enable required services
gcloud services enable \
  aiplatform.googleapis.com \
  storage.googleapis.com \
  bigquery.googleapis.com \
  monitoring.googleapis.com \
  --project=$PROJECT_ID

# Create service account
gcloud iam service-accounts create healthvision-ml \
  --display-name="HealthVision ML Service Account" \
  --project=$PROJECT_ID

# Assign roles
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:healthvision-ml@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/aiplatform.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:healthvision-ml@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/storage.admin"

# Create storage bucket
gsutil mb -l $REGION gs://$PROJECT_ID-healthvision-ml

# Create BigQuery dataset
bq --location=$REGION mk --dataset $PROJECT_ID:healthvision_metrics

echo "GCP setup completed for project $PROJECT_ID"