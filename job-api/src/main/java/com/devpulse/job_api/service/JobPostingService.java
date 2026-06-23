package com.devpulse.job_api.service;

import com.devpulse.job_api.model.JobPosting;
import com.devpulse.job_api.model.User;
import com.devpulse.job_api.repository.JobPostingRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class JobPostingService {

    @Autowired
    JobPostingRepository jobPostingRepository;


    public List<JobPosting> getByJobTitle(String title) {
        return jobPostingRepository.findByTitle(title);
    }


    public List<JobPosting> getActiveJobPostings() {
        return jobPostingRepository.findByIsActive(true);
    }

    public List<JobPosting> getJobPostingsByCompanyName(String companyName) {
        return jobPostingRepository.findByCompanyName(companyName);
    }

    public List<JobPosting> getJobPostingBySkills(List<String> skills) {
       return jobPostingRepository.findBySkillNames(skills);
    }





}


