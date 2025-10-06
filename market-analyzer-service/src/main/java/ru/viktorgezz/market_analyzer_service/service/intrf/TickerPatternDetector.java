package ru.viktorgezz.market_analyzer_service.service.intrf;

import org.ta4j.core.BarSeries;
import ru.viktorgezz.market_analyzer_service.model.PatternFlags;

public interface TickerPatternDetector {

    PatternFlags detectFlagsFor(int index, BarSeries series);
}
