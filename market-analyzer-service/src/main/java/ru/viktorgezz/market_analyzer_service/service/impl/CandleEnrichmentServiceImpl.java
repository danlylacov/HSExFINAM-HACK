package ru.viktorgezz.market_analyzer_service.service.impl;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;
import org.ta4j.core.BarSeries;
import ru.viktorgezz.market_analyzer_service.converter.Ta4jConverter;
import ru.viktorgezz.market_analyzer_service.model.Candle;
import ru.viktorgezz.market_analyzer_service.service.intrf.CandleEnrichmentService;
import ru.viktorgezz.market_analyzer_service.service.intrf.ReceiveCandles;
import ru.viktorgezz.market_analyzer_service.service.intrf.TickerIndicatorCalculator;
import ru.viktorgezz.market_analyzer_service.service.intrf.TickerPatternDetector;

import java.util.List;
import java.util.Map;

@Service
@RequiredArgsConstructor
public class CandleEnrichmentServiceImpl implements CandleEnrichmentService {

    private final ReceiveCandles receiveCandles;
    private final TickerIndicatorCalculator tickerIndicatorCalculator;
    private final TickerPatternDetector tickerPatternDetector;

    @Override
    public Map<String, List<Candle>> calculateAllIndicators(MultipartFile fileCandles) {
        Map<String, List<Candle>> candlesByTicker = receiveCandles.processCandlesByTicker(fileCandles);

        candlesByTicker.forEach(this::enrichCandlesWithIndicators);

        return candlesByTicker;
    }

    private void enrichCandlesWithIndicators(String ticker, List<Candle> candles) {
        if (candles == null || candles.isEmpty()) {
            return;
        }

        BarSeries series = Ta4jConverter.convertToBarSeries(ticker, candles);

        for (int index = 0; index <= tickerIndicatorCalculator.getEndIndex(series); index++) {
            Candle currentCandle = candles.get(index);

            currentCandle.setIndicators(tickerIndicatorCalculator.getIndicatorValuesFor(index, series));
            currentCandle.setPatterns(tickerPatternDetector.detectFlagsFor(index, series));
        }
    }
}
