package com.healthvision.apigateway.service;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
class GatewayServiceTest {

    @Autowired
    private GatewayService gatewayService;

    @Test
    void routeRequest_ShouldReturnCorrectMessage() {
        String result = gatewayService.routeRequest("image-service");
        assertEquals("Routing to image-service", result);
    }
}