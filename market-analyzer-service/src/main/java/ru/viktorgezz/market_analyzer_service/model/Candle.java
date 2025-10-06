package ru.viktorgezz.market_analyzer_service.model;

import lombok.Data;
import lombok.RequiredArgsConstructor;
import ru.viktorgezz.market_analyzer_service.dto.CandleDtoRq;

import java.math.BigDecimal;
import java.time.LocalDate;

@RequiredArgsConstructor
@Data
public class Candle {

    private final BigDecimal open;
    private final BigDecimal close;
    private final BigDecimal high;
    private final BigDecimal low;
    private final BigDecimal volume;
    private final LocalDate date;

    private IndicatorValues indicators;
    private PatternFlags patterns;

    public static Candle from(CandleDtoRq dto) {
        return new Candle(
                BigDecimal.valueOf(dto.getOpen()),
                BigDecimal.valueOf(dto.getClose()),
                BigDecimal.valueOf(dto.getHigh()),
                BigDecimal.valueOf(dto.getLow()),
                BigDecimal.valueOf(dto.getVolume()),
                dto.getBegin()
        );
    }


}
