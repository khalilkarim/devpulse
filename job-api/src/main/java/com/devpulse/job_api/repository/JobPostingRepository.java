package com.devpulse.job_api.repository;

import com.devpulse.job_api.model.JobPosting;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface JobPostingRepository extends JpaRepository<JobPosting, Long> {
    List<JobPosting> findByTitle(String title);
    List<JobPosting> findByPostedAt(LocalDateTime postedAt);
    List<JobPosting> findByCompanyName(String name);
    List<JobPosting> findByTopicName(String name);
    List<JobPosting> findByIsActiveTrue(Boolean isActive);

    @Query("SELECT j FROM JobPosting j JOIN j.skills s WHERE s.name = :skill")
    List<JobPosting> findBySkillName(@Param("skill") String skillName);

    @Query("SELECT j FROM JobPosting j JOIN j.skills s WHERE s.name IN :skills")
    List<JobPosting> findBySkillNames(@Param("skills") List<String> skillNames);
}
