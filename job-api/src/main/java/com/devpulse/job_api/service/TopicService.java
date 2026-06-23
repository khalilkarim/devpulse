package com.devpulse.job_api.service;

import com.devpulse.job_api.model.Topic;
import com.devpulse.job_api.repository.TopicRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class TopicService {
    @Autowired
    TopicRepository topicRepository;

    public Optional<Topic> getTopic(String topicName) {
        existsByName(topicName);
       return topicRepository.findByName(topicName);
    }


    private Boolean existsByName(String name) {
        if (!topicRepository.existsByName(name)) {
            throw new RuntimeException("Topic not found");
        }
        return true;
    }
}
