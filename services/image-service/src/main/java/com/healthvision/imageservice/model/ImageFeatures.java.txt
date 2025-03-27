package com.healthvision.imageservice.model;

import lombok.Data;

@Data
public class ImageFeatures {
    private double[] pixelData;
    private String imageType;
    private int width;
    private int height;
}