package com.devpulse.job_api;

import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
public class JobApiApplication {

	public static void main(String[] args) {
		SpringApplication.run(JobApiApplication.class, args);

	}

	@Bean
	public CommandLineRunner checkFilterBean(ApplicationContext ctx) {
		return args -> System.out.println(
				">>> jwtAuthFilter registered: " + ctx.containsBean("jwtAuthFilter"));
	}

}
