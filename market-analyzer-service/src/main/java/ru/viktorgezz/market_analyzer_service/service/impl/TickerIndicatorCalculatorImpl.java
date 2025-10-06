package ru.viktorgezz.market_analyzer_service.service.impl;

import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.ta4j.core.BarSeries;
import org.ta4j.core.indicators.CCIIndicator;
import org.ta4j.core.indicators.EMAIndicator;
import org.ta4j.core.indicators.MACDIndicator;
import org.ta4j.core.indicators.RSIIndicator;
import org.ta4j.core.indicators.helpers.ClosePriceIndicator;
import org.ta4j.core.num.Num;
import ru.viktorgezz.market_analyzer_service.model.IndicatorValues;
import ru.viktorgezz.market_analyzer_service.service.intrf.TickerIndicatorCalculator;

import java.math.BigDecimal;
import java.math.MathContext;

/**
 * Инкапсулирует всю логику расчета индикаторов TA4j для одной серии свечей (одного тикера).
 */
@Slf4j
@Service
public class TickerIndicatorCalculatorImpl implements TickerIndicatorCalculator {

    public IndicatorValues getIndicatorValuesFor(int index, BarSeries series) {
        ClosePriceIndicator closePrice = new ClosePriceIndicator(series);

        BigDecimal rsi = toBigDecimal(new RSIIndicator(closePrice, 14).getValue(index));
        if (index == 0 || index == 1) {
            rsi = new BigDecimal(50);
        }

        return new IndicatorValues(
                rsi,
                toBigDecimal(new MACDIndicator(closePrice, 12, 26).getValue(index)),
                toBigDecimal(new CCIIndicator(series, 20).getValue(index)),
                toBigDecimal(new EMAIndicator(closePrice, 9).getValue(index)),
                toBigDecimal(new EMAIndicator(closePrice, 50).getValue(index))
        );
    }

    private BigDecimal toBigDecimal(Num num) {
        if (num == null || num.isNaN()) {
            return null;
        }
        Number delegate = num.getDelegate();
        if (delegate instanceof BigDecimal) {
            return (BigDecimal) delegate;
        } else {
            try {
                return new BigDecimal(delegate.toString(), MathContext.DECIMAL64);
            } catch (NumberFormatException e) {
                log.error("Число: {} не удалось перевести в BigDecimal", num);
                return null;
            }
        }
    }

    public long getEndIndex(BarSeries series) {
        return series.getEndIndex();
    }
}