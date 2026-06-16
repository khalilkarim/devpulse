package com.devpulse.job_api.model;

import jakarta.persistence.*;
import lombok.Data;

import java.time.LocalDateTime;

@Entity
@Data
@Table(name = "saved_trends")
public class SavedTrend {

    @EmbeddedId
    private SavedTrendId id;

    @ManyToOne
    @MapsId("userId")
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    @ManyToOne
    @MapsId("trendId")
    @JoinColumn(name = "trend_id", nullable = false)
    private MarketTrend marketTrend;

    @Column(name = "saved_at", nullable = false)
    private LocalDateTime savedAt;

    @PrePersist
    private void onCreate() { savedAt = LocalDateTime.now(); }
}
