package com.healthvision.imageservice.service;

import com.google.cloud.storage.*;
import com.healthvision.imageservice.model.*;
import com.healthvision.imageservice.repository.ImageRepository;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.UUID;

@Service
public class ImageService {
    
    private final ImageRepository repository;
    private final Storage storage;
    
    @Value("${gcs.bucket.name}")
    private String bucketName;
    
    public ImageService(ImageRepository repository, Storage storage) {
        this.repository = repository;
        this.storage = storage;
    }
    
    public ImageAnalysis processImage(MultipartFile file, String patientId) throws IOException {
        String imageId = UUID.randomUUID().toString();
        String gcsPath = storeInGcs(file, imageId);
        
        MedicalImage image = new MedicalImage();
        image.setId(imageId);
        image.setPatientId(patientId);
        image.setOriginalPath(gcsPath);
        repository.save(image);
        
        return new ImageAnalysis(imageId, "Analysis complete");
    }
    
    private String storeInGcs(MultipartFile file, String imageId) throws IOException {
        String objectName = "images/" + imageId;
        BlobId blobId = BlobId.of(bucketName, objectName);
        BlobInfo blobInfo = BlobInfo.newBuilder(blobId).build();
        storage.create(blobInfo, file.getBytes());
        return "gs://" + bucketName + "/" + objectName;
    }
}