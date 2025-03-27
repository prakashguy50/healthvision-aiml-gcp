from google.cloud import aiplatform
import numpy as np

class ModelServer:
    def __init__(self, project: str, location: str, endpoint_id: str):
        aiplatform.init(project=project, location=location)
        self.endpoint = aiplatform.Endpoint(endpoint_id)
        
    def predict(self, features: dict) -> dict:
        """Make prediction using Vertex AI endpoint."""
        instance = [features]
        response = self.endpoint.predict(instances=instance)
        return {
            'predictions': response.predictions[0],
            'model_id': response.deployed_model_id
        }

if __name__ == "__main__":
    # Example usage
    server = ModelServer(
        project="your-project",
        location="us-central1",
        endpoint_id="your-endpoint-id"
    )
    print(server.predict({'feature1': 0.5, 'feature2': 0.8}))