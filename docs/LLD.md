# Low-Level Design

## Image Service Details

### Class Diagram
```plantuml
class ImageController {
  +uploadImage()
  +getAnalysis()
}

class ImageService {
  +processImage()
  +extractFeatures()
}

class ImageRepository {
  +save()
  +findById()
}

ImageController --> ImageService
ImageService --> ImageRepository
ImageService --> MLClient
```

API Specifications
POST /api/images
json
Copy
{
  "image": "base64encoded",
  "patient_id": "12345",
  "priority": "HIGH|NORMAL|LOW"
}
GET /api/images/{id}/analysis
json
Copy
{
  "image_id": "uuid",
  "findings": "text",
  "diagnosis": "text",
  "confidence": 0.95,
  "llm_insights": "text"
}