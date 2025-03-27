# High Level Design

## Architecture Overview
![System Architecture](diagrams/architecture.png)

### Components
1. **API Gateway**: Spring Cloud Gateway
2. **Image Service**: Processes medical images
3. **ML Service**: Hosts trained models
4. **LLM Service**: Provides diagnostic insights
5. **GCP Services**:
   - Cloud Storage: Image storage
   - Pub/Sub: Event streaming
   - Vertex AI: Model training/serving

## Data Flow
1. Image uploaded → Cloud Storage
2. Processing event → Image Service
3. Features → ML Model → Results
4. Results + LLM analysis → Database