package ru.viktorgezz.collector_of_all_data.model;

import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public enum ProcessingStatus {
    INITIATED("Processing initiated"),
    NEWS_PROCESSING("News file processing"),
    CANDLE_PROCESSING("Candle file processing"),
    READY_FOR_PREDICTION("Ready for prediction"),
    PREDICTION_IN_PROGRESS("Prediction in progress"),
    COMPLETED("Processing completed"),
    FAILED("Processing failed");

    private final String description;
}
