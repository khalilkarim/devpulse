package com.devpulse.job_api.repository;

import com.devpulse.job_api.model.SavedJobPosting;
import com.devpulse.job_api.model.SavedJobPostingId;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface SavedJobPostingRepository extends JpaRepository<SavedJobPosting, SavedJobPostingId> {
    List<SavedJobPosting> findByUserId(Long userId);
    List<SavedJobPosting> findBySavedAt(LocalDateTime savedAt);


}
