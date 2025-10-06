package ru.viktorgezz.collector_of_all_data.model;

import lombok.*;

import java.time.LocalDateTime;
import java.util.UUID;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ProcessingSession {
    private String sessionId;
    private ProcessingStatus status;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
    private String newsData;
    private String candleData;
    private String predictionResult;
    private String errorMessage;

    public static ProcessingSession create() {
        LocalDateTime now = LocalDateTime.now();
        return ProcessingSession.builder()
                .sessionId(UUID.randomUUID().toString())
                .status(ProcessingStatus.INITIATED)
                .createdAt(now)
                .updatedAt(now)
                .build();
    }

    public boolean isReadyForPrediction() {
        return newsData != null && candleData != null;
    }

    public void updateStatus(ProcessingStatus newStatus) {
        this.status = newStatus;
        this.updatedAt = LocalDateTime.now();
    }
}
