package com.healthvision.imageservice.model;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Entity
public class MedicalImage {
    @Id
    private String id;
    private String patientId;
    private String originalPath;
    private String findings;
    private LocalDateTime createdAt;
}