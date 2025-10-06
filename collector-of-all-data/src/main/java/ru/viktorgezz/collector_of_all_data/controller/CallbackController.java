package ru.viktorgezz.collector_of_all_data.controller;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import ru.viktorgezz.collector_of_all_data.service.DataProcessingService;

import java.util.Map;

@Slf4j
@RestController
@RequestMapping("/api/v1/callbacks")
@RequiredArgsConstructor
@Tag(name = "Callback-и", description = "Эндпоинты для приёма callback-уведомлений от внешних сервисов")
public class CallbackController {

    private final DataProcessingService dataProcessingService;

    @Operation(
            summary = "Callback от сервиса обработки новостей",
            description = "Принимает результат обработки новостей (Python сервис).",
            responses = {
                    @ApiResponse(responseCode = "200", description = "Callback обработан успешно")
            }
    )
    @PostMapping("/news")
    public ResponseEntity<Map<String, String>> handleNewsCallback(@RequestBody Map<String, String> payload) {
        String sessionId = payload.get("sessionId");
        String status = payload.get("status");

        log.info("Received news callback for session: {}, status: {}", sessionId, status);

        if ("success".equals(status)) {
            dataProcessingService.handleNewsCallback(sessionId, payload.get("data"));
            return ResponseEntity.ok(Map.of("message", "News callback processed successfully"));
        } else {
            dataProcessingService.handleProcessingError(sessionId, "News processing failed: " + payload.getOrDefault("errorMessage", "Unknown error"));
            return ResponseEntity.ok(Map.of("message", "News callback error processed"));
        }
    }

    @Operation(
            summary = "Callback от сервиса обогащения свечей",
            description = "Принимает данные обогащённых свечей от внешнего Spring сервиса.",
            responses = {
                    @ApiResponse(responseCode = "200", description = "Callback обработан успешно")
            }
    )
    @PostMapping("/candles")
    public ResponseEntity<Map<String, String>> handleCandleCallback(@RequestBody Map<String, String> payload) {
        String sessionId = payload.get("sessionId");
        String status = payload.get("status");

        log.info("Received candle callback for session: {}, status: {}", sessionId, status);

        if ("success".equals(status)) {
            dataProcessingService.handleCandleCallback(sessionId, payload.get("data"));
            return ResponseEntity.ok(Map.of("message", "Candle callback processed successfully"));
        } else {
            dataProcessingService.handleProcessingError(sessionId, "Candle processing failed: " + payload.getOrDefault("errorMessage", "Unknown error"));
            return ResponseEntity.ok(Map.of("message", "Candle callback error processed"));
        }
    }

    @Operation(
            summary = "Callback от сервиса предсказаний",
            description = "Принимает результаты предсказаний цен от Python сервиса.",
            responses = {
                    @ApiResponse(responseCode = "200", description = "Callback обработан успешно")
            }
    )
    @PostMapping("/prediction")
    public ResponseEntity<Map<String, String>> handlePredictionCallback(@RequestBody Map<String, String> payload) {
        String sessionId = payload.get("sessionId");
        String status = payload.get("status");

        log.info("Received prediction callback for session: {}, status: {}", sessionId, status);

        if ("success".equals(status)) {
            dataProcessingService.handlePredictionCallback(sessionId, payload.get("prediction"));
            return ResponseEntity.ok(Map.of("message", "Prediction callback processed successfully"));
        } else {
            dataProcessingService.handleProcessingError(sessionId, "Prediction failed: " + payload.getOrDefault("errorMessage", "Unknown error"));
            return ResponseEntity.ok(Map.of("message", "Prediction callback error processed"));
        }
    }
}
