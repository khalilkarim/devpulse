package com.devpulse.job_api.model;

import jakarta.persistence.*;
import lombok.Data;

import java.util.HashSet;
import java.util.Set;

@Entity
@Data
@Table(name = "skills")
public class Skill {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToMany(mappedBy = "skills")
    private Set<JobPosting> jobPostings = new HashSet<>();

    @ManyToMany(mappedBy = "skills")
    private Set<User> users = new HashSet<>();

    @Column(nullable = false)
    private String name;
}
