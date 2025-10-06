package ru.viktorgezz.collector_of_all_data.client;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Component;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;

@Slf4j
@Component
@RequiredArgsConstructor
public class RestExternalServiceClient implements ExternalServiceClient {

    private final RestTemplate restTemplate;

    @Override
    public void sendFileWithCallback(
            MultipartFile file,
            String serviceUrl,
            String callbackUrl,
            String sessionId
    ) {
        try {
            MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
            body.add("file", new ByteArrayResource(file.getBytes()) {
                @Override
                public String getFilename() {
                    return file.getOriginalFilename();
                }
            });
            body.add("callbackUrl", callbackUrl);
            body.add("sessionId", sessionId);

            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.MULTIPART_FORM_DATA);

            HttpEntity<MultiValueMap<String, Object>> requestEntity = new HttpEntity<>(body, headers);

            log.info("Sending file {} to service {} with callback URL {} and sessionId {}",
                    file.getOriginalFilename(), serviceUrl, callbackUrl, sessionId);

            restTemplate.postForEntity(serviceUrl, requestEntity, String.class);

            log.info("File sent successfully to {}", serviceUrl);

        } catch (IOException e) {
            log.error("Error reading file content for sessionId {}", sessionId);
            throw new RuntimeException("Failed to read file content: " + e.getMessage());
        } catch (HttpClientErrorException e) {
            log.error("HTTP error while sending file: {} - {}", e.getStatusCode(), e.getResponseBodyAsString());
            throw new RuntimeException("Failed to send file to external service: " + e.getMessage(), e);
        }
        catch (Exception e) {
            log.error("Error sending file to external service {} for sessionId {}, {}", serviceUrl, sessionId, e.getMessage());
            throw new RuntimeException("Failed to send file to external service", e);
        }
    }

    @Override
    public void sendJsonWithCallback(String jsonData, String serviceUrl, String callbackUrl, String sessionId) {
        try {
            MultiValueMap<String, String> body = new LinkedMultiValueMap<>();
            body.add("data", jsonData);
            body.add("callbackUrl", callbackUrl);
            body.add("sessionId", sessionId);

            log.info("\nRequest body: {}\n\nALL", body);


            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_FORM_URLENCODED);

            HttpEntity<MultiValueMap<String, String>> requestEntity = new HttpEntity<>(body, headers);

            log.info("Sending JSON data to service {} with callback URL {} and sessionId {}",
                    serviceUrl, callbackUrl, sessionId);

            restTemplate.postForEntity(serviceUrl, requestEntity, String.class);

            log.info("JSON data sent successfully to {}", serviceUrl);

        } catch (Exception e) {
            log.error("Error sending JSON to external service {} for sessionId {}", serviceUrl, sessionId);
            throw new RuntimeException("Failed to send JSON to external service");
        }
    }
}