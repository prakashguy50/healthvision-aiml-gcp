output "gcs_bucket_name" {
  value = google_storage_bucket.healthvision_data.name
}

output "k8s_cluster_name" {
  value = google_kubernetes_cluster.healthvision_cluster.name
}

output "pubsub_topic_name" {
  value = google_pubsub_topic.image_processed.name
}