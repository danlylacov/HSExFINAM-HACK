package ru.viktorgezz.market_analyzer_service.converter;

import lombok.extern.slf4j.Slf4j;
import org.ta4j.core.BarSeries;
import org.ta4j.core.BaseBarSeries;
import ru.viktorgezz.market_analyzer_service.model.Candle;

import java.time.LocalDate;
import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.util.List;

/**
 * Утилитарный класс для преобразования данных в форматы, совместимые с библиотекой TA4J.
 */
@Slf4j
public final class Ta4jConverter {

    public static BarSeries convertToBarSeries(String ticker, List<Candle> candles) {
        BarSeries series = new BaseBarSeries(ticker);

        for (Candle candle : candles) {
            LocalDate localDate = candle.getDate();

            ZonedDateTime endTime = localDate.atStartOfDay(ZoneId.systemDefault());

            try {
                series.addBar(
                        endTime,
                        candle.getOpen(),
                        candle.getHigh(),
                        candle.getLow(),
                        candle.getClose(),
                        candle.getVolume()
                );
            } catch (IllegalArgumentException e) {
                log.error("Ошибка: {}, \nсообщения: {}", e.getMessage(), e.getStackTrace());
            }
        }

        return series;
    }

    private Ta4jConverter() {
        throw new UnsupportedOperationException("This is a utility class and cannot be instantiated");
    }
}
