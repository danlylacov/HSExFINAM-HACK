package ru.viktorgezz.market_analyzer_service.model;

import java.math.BigDecimal;

public record IndicatorValues (
        BigDecimal rsi,
        BigDecimal macd,
        BigDecimal cci,
        BigDecimal ema9,
        BigDecimal ema50
) {}
