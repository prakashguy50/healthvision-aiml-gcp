package com.healthvision.imageservice.repository;

import com.healthvision.imageservice.model.MedicalImage;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ImageRepository extends JpaRepository<MedicalImage, String> {
}