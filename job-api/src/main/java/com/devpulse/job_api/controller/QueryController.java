package com.devpulse.job_api.controller;

import com.devpulse.job_api.dto.QueryRequest;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/conversations")
public class QueryController {
    @PostMapping("/ask")
    ResponseEntity<?> ask(@Valid @RequestBody QueryRequest request, Authentication auth) {
        System.out.println("CONTROLLER REACHED");
        String email = auth.getName();
        String query = request.getQuery();


        return ResponseEntity.ok(query);


    }
}
