package com.devpulse.job_api.controller;

import com.devpulse.job_api.dto.AuthResponse;
import com.devpulse.job_api.dto.LoginRequest;
import com.devpulse.job_api.dto.RegisterRequest;
import com.devpulse.job_api.service.AuthService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/auth")
public class AuthController {
    @Autowired
    AuthService authService;


    @PostMapping("/register")
    ResponseEntity<AuthResponse> register(@RequestBody @Valid RegisterRequest request) {

        return  ResponseEntity.status(201).body(authService.register(request));

    }

    @PostMapping("/login")
    ResponseEntity<AuthResponse> login(@RequestBody @Valid LoginRequest request) {

        return ResponseEntity.ok(authService.login(request));
    }


}
