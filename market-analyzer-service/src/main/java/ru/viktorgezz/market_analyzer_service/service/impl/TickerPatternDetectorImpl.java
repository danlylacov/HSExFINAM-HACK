package ru.viktorgezz.market_analyzer_service.service.impl;

import org.springframework.stereotype.Service;
import org.ta4j.core.BarSeries;
import org.ta4j.core.indicators.candles.*;
import ru.viktorgezz.market_analyzer_service.model.PatternFlags;
import ru.viktorgezz.market_analyzer_service.service.intrf.TickerPatternDetector;

@Service
public class TickerPatternDetectorImpl implements TickerPatternDetector {

    @Override
    public PatternFlags detectFlagsFor(int index, BarSeries series) {
        return new PatternFlags(
                new BullishEngulfingIndicator(series).getValue(index),
                new BearishEngulfingIndicator(series).getValue(index),
                new ThreeWhiteSoldiersIndicator(series, 3, series.numOf(0.3)).getValue(index),
                new ThreeBlackCrowsIndicator(series, 3, 0.3).getValue(index),
                new DojiIndicator(series, 3, 0.05).getValue(index)
        );
    }

}
