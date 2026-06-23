package com.devpulse.job_api.service;

import com.devpulse.job_api.model.JobPosting;
import com.devpulse.job_api.model.SavedJobPosting;
import com.devpulse.job_api.model.User;
import com.devpulse.job_api.repository.SavedCompanyRepository;
import com.devpulse.job_api.repository.SavedJobPostingRepository;
import com.devpulse.job_api.repository.SavedTrendRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Service
public class SavedItemService {
    @Autowired
    SavedJobPostingRepository savedJobPostingRepository;

    @Autowired
    SavedTrendRepository savedTrendRepository;

    @Autowired
    SavedCompanyRepository savedCompanyRepository;

    @Autowired
    UserService userService;

    public Optional<SavedJobPosting> getSavedJobPosting(String email, Long jobPostingId) {
       User user = userService.findByEmail(email);
       List<SavedJobPosting> savedJobPostings = savedJobPostingRepository.findByUserId(user.getId());

        Optional<SavedJobPosting> savedJobPosting = savedJobPostings.stream()
               .filter(jobPosting -> jobPosting.getId().equals(jobPostingId)).findFirst();

        return savedJobPosting;

    }


}
