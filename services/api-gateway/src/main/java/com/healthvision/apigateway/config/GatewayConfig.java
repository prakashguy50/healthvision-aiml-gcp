package com.healthvision.apigateway.config;

import org.springframework.cloud.gateway.route.RouteLocator;
import org.springframework.cloud.gateway.route.builder.RouteLocatorBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class GatewayConfig {
    
    @Bean
    public RouteLocator customRouteLocator(RouteLocatorBuilder builder) {
        return builder.routes()
            .route("image-service", r -> r.path("/api/images/**")
                .uri("lb://image-service"))
            .route("llm-service", r -> r.path("/api/llm/**")
                .uri("lb://llm-service"))
            .build();
    }
}