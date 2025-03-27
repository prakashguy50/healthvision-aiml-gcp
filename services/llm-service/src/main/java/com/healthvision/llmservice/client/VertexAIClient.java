package com.healthvision.llmservice.client;

import com.google.cloud.vertexai.VertexAI;
import com.google.cloud.vertexai.api.GenerateContentResponse;
import com.google.cloud.vertexai.generativeai.ContentMaker;
import com.google.cloud.vertexai.generativeai.GenerativeModel;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
public class VertexAIClient {
    
    @Value("${gcp.project.id}")
    private String projectId;
    
    @Value("${gcp.region}")
    private String location;
    
    @Value("${vertex.ai.model}")
    private String modelName;
    
    public String generateContent(String prompt) {
        try (VertexAI vertexAI = new VertexAI(projectId, location)) {
            GenerativeModel model = new GenerativeModel(modelName, vertexAI);
            GenerateContentResponse response = model.generateContent(
                ContentMaker.fromMultiModalData(
                    PartMaker.fromText(prompt)
                )
            );
            return response.getCandidates(0).getContent().getParts(0).getText();
        } catch (Exception e) {
            throw new RuntimeException("Failed to generate content", e);
        }
    }
}