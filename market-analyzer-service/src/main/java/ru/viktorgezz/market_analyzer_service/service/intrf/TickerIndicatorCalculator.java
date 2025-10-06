package ru.viktorgezz.market_analyzer_service.service.intrf;

import org.ta4j.core.BarSeries;
import ru.viktorgezz.market_analyzer_service.model.IndicatorValues;

public interface TickerIndicatorCalculator {

    IndicatorValues getIndicatorValuesFor(int index, BarSeries series);

    long getEndIndex(BarSeries series);
}
