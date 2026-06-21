package com.devpulse.job_api.service;

import com.devpulse.job_api.model.User;
import com.devpulse.job_api.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class UserService {
    @Autowired
    UserRepository userRepository;

    public User findByEmail(String email) {
        if (!userRepository.existsByEmail(email)) {
            throw new RuntimeException("User not found");
        }
       return userRepository.findByEmail(email)
               .orElseThrow(() -> new RuntimeException("User not found"));
    }

    public Boolean validateEmailNotTaken(String email) {
        if (existsByEmail(email)) {
            throw new RuntimeException("Email already taken");
        }

        return false;
    }



    private Boolean existsByEmail(String email) {
        return userRepository.existsByEmail(email);

    }

}
