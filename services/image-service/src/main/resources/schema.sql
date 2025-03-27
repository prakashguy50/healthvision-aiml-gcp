CREATE TABLE IF NOT EXISTS medical_images (
    id VARCHAR(36) PRIMARY KEY,
    patient_id VARCHAR(255) NOT NULL,
    original_path VARCHAR(1024) NOT NULL,
    findings TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);