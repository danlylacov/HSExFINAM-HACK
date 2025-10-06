package ru.viktorgezz.collector_of_all_data.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class PredictionResponse {
    private String sessionId;
    private String predictionResult;
    private ProcessingStatus status;
    private LocalDateTime completedAt;
    private String errorMessage;
    private String csvBase64;
}
