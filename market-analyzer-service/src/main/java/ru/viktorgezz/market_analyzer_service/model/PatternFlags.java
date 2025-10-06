package ru.viktorgezz.market_analyzer_service.model;

public record PatternFlags(
        boolean isBullishEngulfing,
        boolean isBearishEngulfing,
        boolean areThreeWhiteSoldiers,
        boolean areThreeBlackCrows,
        boolean isDoji
) {
}
