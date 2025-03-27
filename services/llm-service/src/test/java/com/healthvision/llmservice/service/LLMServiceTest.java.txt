package com.healthvision.llmservice.service;

import com.healthvision.llmservice.client.VertexAIClient;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class LLMServiceTest {

    @Mock
    private VertexAIClient vertexAIClient;

    @InjectMocks
    private LLMService llmService;

    @Test
    void generateDiagnosticReport_ShouldCallClient() {
        when(vertexAIClient.generateContent(anyString())).thenReturn("test response");

        String result = llmService.generateDiagnosticReport("test findings");
        
        assertEquals("test response", result);
        verify(vertexAIClient, times(1)).generateContent(anyString());
    }
}