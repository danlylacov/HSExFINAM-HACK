package ru.viktorgezz.market_analyzer_service.converter;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;
import org.springframework.web.multipart.MultipartFile;
import ru.viktorgezz.market_analyzer_service.dto.CandleDtoRs;
import ru.viktorgezz.market_analyzer_service.model.Candle;
import ru.viktorgezz.market_analyzer_service.service.intrf.CandleEnrichmentService;

import java.util.ArrayList;
import java.util.List;

@Component
@RequiredArgsConstructor
public class ConverterCsvToList implements ConverterCsv {

    private final CandleEnrichmentService candleService;

    public List<CandleDtoRs> calculateIndicatorsAndPatterns(MultipartFile fileCandles) {
        List<CandleDtoRs> recordsToWrite = new ArrayList<>();
        candleService.calculateAllIndicators(fileCandles)
                .forEach((ticker, candles) -> {
                    for (Candle candle : candles) {
                        recordsToWrite.add(
                                CandleDtoRs.ConvertToCandleDtoRs(candle, ticker)
                        );
                    }
                });

        return recordsToWrite;
    }
}
