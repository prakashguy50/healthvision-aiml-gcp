package com.healthvision.llmservice.service;

import com.healthvision.llmservice.client.VertexAIClient;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class LLMService {
    private final VertexAIClient vertexAIClient;

    public String generateDiagnosticReport(String findings) {
        try {
            String prompt = "As a medical expert, analyze these ultrasound findings:\n" + 
                          findings + "\n\nProvide:\n1. Potential diagnoses\n" +
                          "2. Confidence levels\n3. Recommended next steps";
            
            return vertexAIClient.generateContent(prompt);
        } catch (Exception e) {
            throw new RuntimeException("Failed to generate diagnostic report", e);
        }
    }
}