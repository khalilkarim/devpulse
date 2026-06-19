package com.devpulse.job_api.repository;

import com.devpulse.job_api.model.Company;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface CompanyRepository extends JpaRepository<Company, Long> {

   Optional<Company> findByName(String name);
    List<Company> findByLocation(String location);
    List<Company> findByApplicationSuccessRateGreaterThan(Double rate);
}
