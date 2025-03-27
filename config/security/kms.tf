resource "google_kms_key_ring" "healthvision" {
  name     = "healthvision-keyring"
  location = "global"
}

resource "google_kms_crypto_key" "dicom" {
  name            = "dicom-encryption-key"
  key_ring        = google_kms_key_ring.healthvision.id
  rotation_period = "7776000s" # 90 days
}