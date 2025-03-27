package com.healthvision.imageservice.model;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class ImageAnalysis {
    private String imageId;
    private String findings;
    private String diagnosis;
    private double confidence;
}