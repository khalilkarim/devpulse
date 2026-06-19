package com.devpulse.job_api.repository;

import com.devpulse.job_api.model.MarketTrend;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface MarketTrendRepository extends JpaRepository<MarketTrend, Long> {
    List<MarketTrend> findByMentionCount(Long mentionCount);
    List<MarketTrend> findByTopicName(String name);
    List<MarketTrend> findBySkillName(String name);
    List<MarketTrend> findBySkillNameAndTopicName(String topicName, String trendName);
    List<MarketTrend> findBySkillNameIn(List<String> skillNames);
    List<MarketTrend> findBySkillNameInAndTopicNameIn(List<String> skillNames, List<String> topicNames);



}
