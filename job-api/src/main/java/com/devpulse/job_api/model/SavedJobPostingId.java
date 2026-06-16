package com.devpulse.job_api.model;

import jakarta.persistence.Column;
import jakarta.persistence.Embeddable;

import java.io.Serializable;

@Embeddable
public class SavedJobPostingId implements Serializable {

    @Column(name = "job_id")
    private Long jobId;

    @Column(name = "user_id")
    private Long userId;

}
