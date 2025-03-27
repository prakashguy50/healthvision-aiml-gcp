package com.healthvision.imageservice.controller;

import com.healthvision.imageservice.service.ImageService;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.test.web.servlet.MockMvc;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(ImageController.class)
class ImageControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private ImageService imageService;

    @Test
    void uploadImage_ShouldReturnOk() throws Exception {
        MockMultipartFile file = new MockMultipartFile(
            "file", "test.dcm", "application/dicom", "test".getBytes());

        mockMvc.perform(multipart("/api/images")
                .file(file)
                .param("patientId", "123"))
                .andExpect(status().isOk());
    }
}