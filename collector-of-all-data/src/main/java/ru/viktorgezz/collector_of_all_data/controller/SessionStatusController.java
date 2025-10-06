package ru.viktorgezz.collector_of_all_data.controller;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import ru.viktorgezz.collector_of_all_data.model.PredictionResponse;
import ru.viktorgezz.collector_of_all_data.model.ProcessingSession;
import ru.viktorgezz.collector_of_all_data.model.ProcessingStatus;
import ru.viktorgezz.collector_of_all_data.service.SessionService;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.Base64;
import java.util.LinkedHashSet;
import java.util.Map;
import java.util.Set;

@Slf4j
@RestController
@RequestMapping("/api/v1/sessions")
@RequiredArgsConstructor
@Tag(name = "Статус обработки", description = "Эндпоинты для проверки статуса и получения результатов обработки")
public class SessionStatusController {

    private final SessionService sessionService;

    @Operation(
            summary = "Проверить статус обработки",
            description = "Возвращает текущий статус обработки по идентификатору `sessionId`.",
            responses = {
                    @ApiResponse(responseCode = "200", description = "Статус успешно получен"),
                    @ApiResponse(responseCode = "404", description = "Сессия не найдена")
            }
    )
    @GetMapping("/{sessionId}/status")
    public ResponseEntity<Map<String, Object>> getStatus(@PathVariable String sessionId) {
        log.info("Status check requested for session: {}", sessionId);

        ProcessingSession session = sessionService.getSession(sessionId);

        return ResponseEntity.ok(Map.of(
                "sessionId", session.getSessionId(),
                "status", session.getStatus(),
                "createdAt", session.getCreatedAt(),
                "updatedAt", session.getUpdatedAt()
        ));
    }

    @Operation(
            summary = "Получить результат предсказания",
            description = "Возвращает результат предсказания, если обработка завершена. Используется для long polling.",
            responses = {
                    @ApiResponse(responseCode = "200", description = "Обработка завершена, результат доступен"),
                    @ApiResponse(responseCode = "202", description = "Обработка ещё не завершена"),
                    @ApiResponse(responseCode = "422", description = "Ошибка обработки")
            }
    )
    @GetMapping("/{sessionId}/result")
    public ResponseEntity<PredictionResponse> getResult(@PathVariable String sessionId) {
        log.info("Result requested for session: {}", sessionId);

        ProcessingSession session = sessionService.getSession(sessionId);

        PredictionResponse.PredictionResponseBuilder responseBuilder = PredictionResponse
                .builder()
                .sessionId(session.getSessionId())
                .status(session.getStatus())
                .predictionResult(session.getPredictionResult())
                .completedAt(session.getUpdatedAt())
                .errorMessage(session.getErrorMessage());

        if (session.getStatus() == ProcessingStatus.COMPLETED && session.getPredictionResult() != null) {
            try {
                String csvContent = convertJsonToCsv(session.getPredictionResult());
                String base64Csv = Base64.getEncoder()
                        .encodeToString(csvContent.getBytes(StandardCharsets.UTF_8));
                responseBuilder.csvBase64(base64Csv);
            } catch (Exception e) {
                log.error("Failed to convert predictionResult to CSV for session {}", sessionId, e);
                responseBuilder.errorMessage("Error generating CSV from predictionResult");
            }
        }

        return switch (session.getStatus()) {
            case COMPLETED -> ResponseEntity.ok(responseBuilder.build());
            case FAILED -> ResponseEntity.status(HttpStatus.UNPROCESSABLE_ENTITY).body(responseBuilder.build());
            default -> ResponseEntity.status(HttpStatus.ACCEPTED).body(responseBuilder.build());
        };
    }

    private String convertJsonToCsv(String jsonString) throws IOException {
        ObjectMapper objectMapper = new ObjectMapper();
        JsonNode rootNode = objectMapper.readTree(jsonString);

        if (!rootNode.isArray()) {
            throw new IllegalArgumentException("Expected JSON array for CSV conversion");
        }

        Set<String> headers = new LinkedHashSet<>();
        for (JsonNode node : rootNode) {
            node.fieldNames().forEachRemaining(headers::add);
        }

        StringBuilder csv = new StringBuilder(String.join(",", headers)).append("\n");

        // Построчно
        for (JsonNode node : rootNode) {
            for (String header : headers) {
                String value = node.has(header) ? node.get(header).asText().replace(",", ".") : "";
                csv.append(value).append(",");
            }
            csv.setLength(csv.length() - 1);
            csv.append("\n");
        }

        return csv.toString();
    }
}
