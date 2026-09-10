package com.devpulse.job_api.dto;

import jakarta.validation.constraints.NotBlank;
import lombok.Data;

@Data
public class QueryRequest {
    @NotBlank(message = "Query cant be empty")
    private String query;
}
