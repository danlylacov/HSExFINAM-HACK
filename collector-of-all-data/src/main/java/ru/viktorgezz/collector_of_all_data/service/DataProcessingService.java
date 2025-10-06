package ru.viktorgezz.collector_of_all_data.service;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;
import ru.viktorgezz.collector_of_all_data.client.ExternalServiceClient;
import ru.viktorgezz.collector_of_all_data.config.ValueConfiguration;
import ru.viktorgezz.collector_of_all_data.model.CombinedData;
import ru.viktorgezz.collector_of_all_data.model.ProcessingSession;

@Slf4j
@Service
@RequiredArgsConstructor
public class DataProcessingService {

    private final ExternalServiceClient externalServiceClient;
    private final SessionService sessionService;
    private final ValueConfiguration valueConfiguration;
    private final ObjectMapper objectMapper;

    public void processNewsFile(MultipartFile newsFile, String sessionId) {
        log.info("Starting news file processing for session: {}", sessionId);

        externalServiceClient.sendFileWithCallback(
                newsFile,
                valueConfiguration.getNewsProcessorUrl(),
                valueConfiguration.getNewsCallbackUrl(),
                sessionId
        );

        log.info("News file sent for processing, session: {}", sessionId);
    }

    public void processCandleFile(MultipartFile candleFile, String sessionId) {
        log.info("Starting candle file processing for session: {}", sessionId);

        externalServiceClient.sendFileWithCallback(
                candleFile,
                valueConfiguration.getCandleEnricherUrl(),
                valueConfiguration.getCandleCallbackUrl(),
                sessionId
        );

        log.info("Candle file sent for processing, session: {}", sessionId);
    }

    public void handleNewsCallback(String sessionId, String processedNewsData) {
        log.info("Received news callback for session: {}", sessionId);

        sessionService.updateNewsData(sessionId, processedNewsData);
        checkAndInitiatePrediction(sessionId);
    }

    public void handleCandleCallback(String sessionId, String processedCandleData) {
        log.info("Received candle callback for session: {}", sessionId);

        sessionService.updateCandleData(sessionId, processedCandleData);
        checkAndInitiatePrediction(sessionId);
    }

    public void handlePredictionCallback(String sessionId, String predictionResult) {
        log.info("Received prediction callback for session: {}", sessionId);
        sessionService.completePrediction(sessionId, predictionResult);
    }

    public void handleProcessingError(String sessionId, String errorMessage) {
        log.error("Processing error for session {}: {}", sessionId, errorMessage);
        sessionService.markFailed(sessionId, errorMessage);
    }

    private void checkAndInitiatePrediction(String sessionId) {
        ProcessingSession session = sessionService.getSession(sessionId);

        if (session.isReadyForPrediction()) {
            log.info("Both files processed, initiating prediction for session: {}", sessionId);
            sessionService.markReadyForPrediction(sessionId);
            sendToPredictionService(session);
        } else {
            log.info("Waiting for other file to complete for session: {}", sessionId);
        }
    }

    private void sendToPredictionService(ProcessingSession session) {
        try {
            sessionService.markPredictionInProgress(session.getSessionId());

            CombinedData combinedData = CombinedData.builder()
                    .sessionId(session.getSessionId())
                    .newsData(session.getNewsData())
                    .candleData(session.getCandleData())
                    .build();

            String jsonData = objectMapper.writeValueAsString(combinedData);
//            log.info("\n\n\n{}\nALL", session.getNewsData());
            //log.info("\n\n\n{}\nALL", jsonData);

            externalServiceClient.sendJsonWithCallback(
                    jsonData,
                    valueConfiguration.getPricePredictorUrl(),
                    valueConfiguration.getPredictionCallbackUrl(),
                    session.getSessionId()
            );

            log.info("Combined data sent to prediction service for session: {}", session.getSessionId());

        } catch (JsonProcessingException e) {
            log.error("Error serializing combined data for session: {}", session.getSessionId(), e);
            sessionService.markFailed(session.getSessionId(), "Failed to serialize combined data: " + e.getMessage());
        } catch (Exception e) {
            log.error("Error sending data to prediction service for session: {}", session.getSessionId(), e);
            sessionService.markFailed(session.getSessionId(), "Failed to send data to prediction service: " + e.getMessage());
        }
    }
}