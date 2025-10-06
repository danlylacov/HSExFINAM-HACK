package ru.viktorgezz.market_analyzer_service.client;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartFile;
import ru.viktorgezz.market_analyzer_service.converter.ConverterCsv;
import ru.viktorgezz.market_analyzer_service.dto.CandleDtoRs;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Slf4j
@Component
@RequiredArgsConstructor
public class ClientCallback {

    private final ConverterCsv converterCsv;
    private final RestTemplate restTemplate;

    public void send(String callbackUrl, String sessionId, MultipartFile fileCandles) {
        try {
            List<CandleDtoRs> candles = converterCsv.calculateIndicatorsAndPatterns(fileCandles);
            Map<String, String> payload = new HashMap<>();
            payload.put("sessionId", sessionId);
            payload.put("status", "success");
            payload.put("data", candles.toString());

            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);

            HttpEntity<Map<String, String>> requestEntity = new HttpEntity<>(payload, headers);
            restTemplate.postForEntity(callbackUrl, requestEntity, Map.class);
        } catch (Exception e) {
            Map<String, String> errorPayload = new HashMap<>();
            errorPayload.put("sessionId", sessionId);
            errorPayload.put("status", "error");
            errorPayload.put("errorMessage", "Failed to process candles: " + e.getMessage());

            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);

            HttpEntity<Map<String, String>> requestEntity = new HttpEntity<>(errorPayload, headers);

            log.error("Error processing candles for sessionId {}", sessionId, e);

            try {
                restTemplate.postForEntity(callbackUrl, requestEntity, Map.class);
                log.info("Error callback sent to {} for sessionId {}", callbackUrl, sessionId);
            } catch (Exception ex) {
                log.error("Failed to send error callback to {} for sessionId {}", callbackUrl, sessionId, ex);
                throw new RuntimeException("Failed to send error callback", ex);
            }
        }
    }
}
