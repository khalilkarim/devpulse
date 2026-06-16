package com.devpulse.job_api.model;

import jakarta.persistence.*;
import lombok.Data;

@Entity
@Data
@Table(name = "topics")
public class Topic {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String name;
}
