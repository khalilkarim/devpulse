package com.devpulse.job_api.repository;

import com.devpulse.job_api.model.SavedCompany;
import com.devpulse.job_api.model.SavedCompanyId;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface SavedCompanyRepository extends JpaRepository<SavedCompany, SavedCompanyId> {
    List<SavedCompany> findBySavedAt(LocalDateTime savedAt);
}
