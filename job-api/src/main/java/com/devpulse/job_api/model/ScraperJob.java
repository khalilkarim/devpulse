package com.devpulse.job_api.model;

import jakarta.persistence.*;
import lombok.Data;

import java.time.LocalDateTime;

@Entity
@Data
@Table(name = "scraper_jobs")
public class ScraperJob {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "search_query", nullable = false)
    private String searchQuery;

    @Column(nullable = false)
    private SourceType source;

    @Column(name = "started_at")
    private LocalDateTime startedAt;

    @Column(name = "ended_at")
    private LocalDateTime endedAt;

    @Column(name = "scrape_successful")
    private Boolean isScrapeSuccessful;

    @Column(name = "jobs_found_count")
    private Long jobsFoundCount;

    @Column(name = "error_message")
    private String errorMessage;

    @Column(name = "next_retry_at")
    private LocalDateTime nextRetryAt;

    @PrePersist
    private void onCreate() { startedAt = LocalDateTime.now(); }
}
