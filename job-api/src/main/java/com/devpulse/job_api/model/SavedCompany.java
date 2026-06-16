package com.devpulse.job_api.model;

import jakarta.persistence.*;
import lombok.Data;

import java.time.LocalDateTime;

@Entity
@Data
@Table(name = "saved_company")
public class SavedCompany {

    @EmbeddedId
    private SavedCompanyId id;

    @ManyToOne
    @MapsId("companyId")
    @JoinColumn(name = "company_id", nullable = false)
    private Company company;

    @ManyToOne
    @MapsId("userId")
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    @Column(name = "saved_at", nullable = false)
    private LocalDateTime savedAt;

    @PrePersist
    private void onCreate() { savedAt = LocalDateTime.now(); }

}
