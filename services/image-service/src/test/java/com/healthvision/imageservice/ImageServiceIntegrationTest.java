package com.healthvision.imageservice;

import com.healthvision.imageservice.model.ImageAnalysis;
import com.healthvision.imageservice.service.ImageService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.mock.web.MockMultipartFile;

import java.io.IOException;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
class ImageServiceIntegrationTest {

    @Autowired
    private ImageService imageService;

    @Test
    void processImage_ShouldReturnAnalysis() throws IOException {
        MockMultipartFile file = new MockMultipartFile(
            "file", "test.dcm", "application/dicom", "test".getBytes());

        ImageAnalysis result = imageService.processImage(file, "123");
        
        assertNotNull(result.getImageId());
        assertNotNull(result.getFindings());
    }
}