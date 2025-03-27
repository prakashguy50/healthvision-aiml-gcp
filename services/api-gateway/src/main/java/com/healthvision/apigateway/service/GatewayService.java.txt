package com.healthvision.apigateway.service;

import org.springframework.stereotype.Service;

@Service
public class GatewayService {
    
    public String routeRequest(String serviceName) {
        return "Routing to " + serviceName;
    }
}