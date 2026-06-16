package com.devpulse.job_api.model;

import jakarta.persistence.*;
import lombok.Data;

import java.util.HashSet;
import java.util.Set;

@Entity
@Data
@Table(name = "companies")
public class Company {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String name;

    @Column(name = "company_site")
    private String companySite;

    @Column
    private String location;

    @Column(name = "application_success_rate")
    private Double applicationSuccessRate;

}
