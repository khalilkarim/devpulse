package com.devpulse.job_api.model;

import jakarta.persistence.*;
import lombok.Data;

import java.time.LocalDateTime;

@Entity
@Data
@Table(name = "market_trends")
public class MarketTrend {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "period_type", nullable = false)
    private PeriodType periodType;

    @Column(name = "mention_count", nullable = false)
    private Long mentionCount;

    @Column(name = "period_start", nullable = false)
    private LocalDateTime periodStart;

    @ManyToOne
    @JoinColumn(name = "topic_id")
    private Topic topic;

    @ManyToOne
    @JoinColumn(name = "skill_id")
    private Skill skill;


}
