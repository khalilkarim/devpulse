package com.devpulse.job_api.model;

import jakarta.persistence.Column;
import jakarta.persistence.Embeddable;

import java.io.Serializable;

@Embeddable
public class SavedCompanyId implements Serializable {
    @Column(name = "company_id")
    private Long companyId;

    @Column(name = "user_id")
    private Long userId;
}
