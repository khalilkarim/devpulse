package com.devpulse.job_api.controller;

import com.devpulse.job_api.dto.AgentRequest;
import com.devpulse.job_api.dto.AgentResponse;
import com.devpulse.job_api.dto.QueryRequest;
import com.devpulse.job_api.model.User;
import com.devpulse.job_api.repository.UserRepository;
import com.devpulse.job_api.service.UserService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

@RestController
@RequestMapping("/conversations")
public class QueryController {

    @Value("${python.agent.url}")
    private String pythonAgentUrl;

    private final RestTemplate restTemplate;
    private final UserService userService;

    public QueryController(RestTemplate restTemplate, UserService userService) {
        this.restTemplate = restTemplate;
        this.userService = userService;
    }

    @PostMapping("/ask")
    ResponseEntity<AgentResponse> ask(@Valid @RequestBody QueryRequest request, Authentication auth) {
        String email = auth.getName();
        User user = userService.findByEmail(email);

        AgentRequest agentRequest = new AgentRequest(user.getId(), request.getQuery());

        AgentResponse response = restTemplate.postForObject(
                pythonAgentUrl, agentRequest, AgentResponse.class);

        return ResponseEntity.ok(response);
    }
}
