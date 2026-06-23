package com.devpulse.job_api.service;

import com.devpulse.job_api.model.MarketTrend;
import com.devpulse.job_api.repository.MarketTrendRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class MarketTrendService {
    @Autowired
    MarketTrendRepository marketTrendRepository;


}
