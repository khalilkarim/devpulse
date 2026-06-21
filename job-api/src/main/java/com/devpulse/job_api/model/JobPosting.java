package com.devpulse.job_api.model;

import jakarta.persistence.*;
import lombok.Data;

import java.time.LocalDateTime;
import java.util.HashSet;
import java.util.Set;

@Entity
@Data
@Table(name = "job_postings")
public class JobPosting {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToMany
    @JoinTable(
            name = "job_posting_skills",
            joinColumns = @JoinColumn(name = "job_id"),
            inverseJoinColumns = @JoinColumn(name = "skill_id")
    )
    private Set<Skill> skills = new HashSet<>();

    @Column(nullable = false)
    private String title;

    @Column
    private String description;

    @Column(nullable = false)
    private String url;

    @Column(nullable = false)
    private SourceType source;

    @Column(name = "is_analyzed")
    private Boolean isAnalyzed;

    @Column(name = "is_active")
    private Boolean isActive;

    @Column(name = "posted_at", nullable = false)
    private LocalDateTime postedAt;

    @Column(name = "scraped_at", nullable = false)
    private LocalDateTime scrapedAt;

    @ManyToOne
    @JoinColumn(name = "topic_id")
    private Topic topic;

    @ManyToOne
    @JoinColumn(name = "company_id")
    private Company company;

    @PrePersist
    private void onCreate() {
        postedAt = LocalDateTime.now();
        scrapedAt = LocalDateTime.now();
    }


}
