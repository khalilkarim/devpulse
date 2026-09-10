package com.devpulse.job_api.dto;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class AgentRequest {

    private Long userId;
    private String query;


}
