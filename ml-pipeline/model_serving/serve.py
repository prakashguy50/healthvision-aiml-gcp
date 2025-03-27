from google.cloud import aiplatform
import numpy as np

class ModelServer:
    def __init__(self, project, location, endpoint_id):
        aiplatform.init(project=project, location=location)
        self.endpoint = aiplatform.Endpoint(endpoint_id)
        
    def predict(self, features):
        """
        Make prediction using Vertex AI endpoint
        """
        instance = [features.tolist()]
        response = self.endpoint.predict(instances=instance)
        return response.predictions[0]

if __name__ == "__main__":
    # Example usage
    server = ModelServer(
        project="your-project",
        location="us-central1",
        endpoint_id="your-endpoint-id"
    )
    sample_input = np.random.rand(1, 224, 224, 3)  # Example input shape
    print(server.predict(sample_input))