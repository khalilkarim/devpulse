package com.devpulse.job_api.security;

import jakarta.annotation.PostConstruct;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.Lazy;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.web.authentication.WebAuthenticationDetailsSource;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;

@Component
public class JwtAuthFilter extends OncePerRequestFilter {


    private final JwtService jwtService;

    private final ApplicationContext applicationContext;

    private UserDetailsService userDetailsService;


    public JwtAuthFilter(ApplicationContext applicationContext, JwtService jwtService) {
        this.applicationContext = applicationContext;
        this.jwtService = jwtService;
    }

    @PostConstruct
    public void init() {
        System.out.println(">>> JwtAuthFilter BEAN CREATED");
    }


    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                    HttpServletResponse response,
                                    FilterChain filterChain
    ) throws ServletException, IOException {
        System.out.println("!!!!!!!!!! FILTER EXECUTING !!!!!!!!!!");
        final String authHeader = request.getHeader("Authorization");
        final String jwt;
        final String email;

        if (authHeader == null || !authHeader.startsWith("Bearer ")) {
            System.out.println(">>> No bearer, skipping");
            filterChain.doFilter(request, response);
            return;
        }

        if (this.userDetailsService == null) {
            this.userDetailsService = applicationContext.getBean(UserDetailsService.class);
        }

        jwt = authHeader.substring(7);
        try {
            email = jwtService.extractEmail(jwt);
            System.out.println("EXTRACTED EMAIL: " + email);
        } catch (Exception e) {
            System.out.println("TOKEN PARSING FAILED: " + e.getClass().getSimpleName() + " - " + e.getMessage());
            filterChain.doFilter(request, response);
            return;
        }

        if (email != null && SecurityContextHolder.getContext().getAuthentication() == null) {
            UserDetails userDetails = userDetailsService.loadUserByUsername(email);

            if (jwtService.isTokenValid(jwt, userDetails.getUsername())) {

                UsernamePasswordAuthenticationToken authToken =
                        new UsernamePasswordAuthenticationToken(
                                userDetails,
                                null,
                                userDetails.getAuthorities()
                        );
                authToken.setDetails(
                        new WebAuthenticationDetailsSource().buildDetails(request)
                );

                SecurityContextHolder.getContext().setAuthentication(authToken);
            }
        }
        filterChain.doFilter(request, response);
    }


}

