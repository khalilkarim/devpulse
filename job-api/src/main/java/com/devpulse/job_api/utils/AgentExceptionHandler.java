package com.devpulse.job_api.utils;
import com.devpulse.job_api.dto.ErrorResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.client.HttpServerErrorException;
import org.springframework.web.client.ResourceAccessException;

@RestControllerAdvice
public class AgentExceptionHandler {

    private static final Logger log = LoggerFactory.getLogger(AgentExceptionHandler.class);

    @ExceptionHandler(ResourceAccessException.class)
    public ResponseEntity<ErrorResponse> handlePythonUnreachable(ResourceAccessException e) {
        log.error("Python service unreachable: {}", e.getMessage());
        return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE)
                .body(new ErrorResponse("Agent service is currently unavailable"));
    }

    @ExceptionHandler(HttpServerErrorException.class)
    public ResponseEntity<ErrorResponse> handleGeminiFailure(HttpServerErrorException e) {
        log.error("Downstream agent failure: status={}, body={}",
                e.getStatusCode(), e.getResponseBodyAsString());
        return ResponseEntity.status(HttpStatus.BAD_GATEWAY)
                .body(new ErrorResponse("Agent service failed to process the request"));
    }
}
