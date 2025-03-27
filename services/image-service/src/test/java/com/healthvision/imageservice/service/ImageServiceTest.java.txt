package com.healthvision.imageservice.service;

import com.google.cloud.storage.Storage;
import com.healthvision.imageservice.model.ImageAnalysis;
import com.healthvision.imageservice.model.MedicalImage;
import com.healthvision.imageservice.repository.ImageRepository;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.mock.web.MockMultipartFile;

import java.io.IOException;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class ImageServiceTest {

    @Mock
    private ImageRepository repository;

    @Mock
    private Storage storage;

    @Mock
    private MLServiceClient mlClient;

    @InjectMocks
    private ImageService imageService;

    @Test
    void processImage_ShouldStoreImage() throws IOException {
        MockMultipartFile file = new MockMultipartFile(
            "file", "test.dcm", "application/dicom", "test".getBytes());

        when(repository.save(any())).thenReturn(new MedicalImage());

        ImageAnalysis result = imageService.processImage(file, "123");

        assertNotNull(result);
        verify(repository, times(1)).save(any());
    }
}