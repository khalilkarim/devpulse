package com.devpulse.job_api.model;

import jakarta.persistence.Column;
import jakarta.persistence.Embeddable;

import java.io.Serializable;

@Embeddable
public class SavedTrendId implements Serializable {

    @Column(name = "user_id", nullable = false)
    private Long userId;

    @Column(name = "trend_id", nullable = false)
    private Long trendId;



}
