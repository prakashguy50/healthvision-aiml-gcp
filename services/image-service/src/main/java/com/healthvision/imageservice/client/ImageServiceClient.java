package com.healthvision.imageservice.client;

import com.healthvision.imageservice.model.ImageFeatures;
import com.healthvision.imageservice.model.MLResult;
import org.springframework.stereotype.Component;

@Component
public class MLServiceClient {
    
    public MLResult predict(ImageFeatures features) {
        // In production, this would call your ML service
        return new MLResult("Normal anatomy", "No abnormalities detected", 0.95);
    }
}