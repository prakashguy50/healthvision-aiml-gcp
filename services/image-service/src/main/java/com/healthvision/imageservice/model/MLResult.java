package com.healthvision.imageservice.model;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class MLResult {
    private String findings;
    private String diagnosis;
    private double confidence;
}