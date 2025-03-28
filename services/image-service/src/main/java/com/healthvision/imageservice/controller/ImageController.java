package com.healthvision.imageservice.controller;

import com.healthvision.imageservice.model.ImageAnalysis;
import com.healthvision.imageservice.service.ImageService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
@RequestMapping("/api/images")
public class ImageController {
    
    private final ImageService imageService;
    
    public ImageController(ImageService imageService) {
        this.imageService = imageService;
    }
    
    @PostMapping
    public ResponseEntity<ImageAnalysis> uploadImage(
            @RequestParam("file") MultipartFile file,
            @RequestParam("patientId") String patientId) {
        return ResponseEntity.ok(imageService.processImage(file, patientId));
    }
    
    @GetMapping("/{id}/analysis")
    public ResponseEntity<ImageAnalysis> getAnalysis(@PathVariable String id) {
        return ResponseEntity.ok(imageService.getAnalysis(id));
    }
}