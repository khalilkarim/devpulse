package com.devpulse.job_api.repository;

import com.devpulse.job_api.model.SavedTrend;
import com.devpulse.job_api.model.SavedTrendId;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface SavedTrendRepository extends JpaRepository<SavedTrend, SavedTrendId> {

    List<SavedTrend> findBySavedAt(LocalDateTime savedAt);
}
