package ru.viktorgezz.market_analyzer_service.dto;

import com.opencsv.bean.CsvBindByName;
import com.opencsv.bean.CsvBindByPosition;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import ru.viktorgezz.market_analyzer_service.model.Candle;

import java.math.BigDecimal;
import java.time.LocalDate;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class CandleDtoRs {

    @CsvBindByName(column = "ticker")
    @CsvBindByPosition(position = 0)
    private String ticker;

    @CsvBindByName(column = "begin")
    @CsvBindByPosition(position = 1)
    private LocalDate begin;

    @CsvBindByName(column = "open")
    @CsvBindByPosition(position = 2)
    private BigDecimal open;

    @CsvBindByName(column = "high")
    @CsvBindByPosition(position = 3)
    private BigDecimal high;

    @CsvBindByName(column = "low")
    @CsvBindByPosition(position = 4)
    private BigDecimal low;

    @CsvBindByName(column = "close")
    @CsvBindByPosition(position = 5)
    private BigDecimal close;

    @CsvBindByName(column = "volume")
    @CsvBindByPosition(position = 6)
    private BigDecimal volume;

    @CsvBindByName(column = "rsi")
    @CsvBindByPosition(position = 7)
    private BigDecimal rsi;

    @CsvBindByName(column = "macd")
    @CsvBindByPosition(position = 8)
    private BigDecimal macd;

    @CsvBindByName(column = "cci")
    @CsvBindByPosition(position = 9)
    private BigDecimal cci;

    @CsvBindByName(column = "ema9")
    @CsvBindByPosition(position = 10)
    private BigDecimal ema9;

    @CsvBindByName(column = "ema50")
    @CsvBindByPosition(position = 11)
    private BigDecimal ema50;

    @CsvBindByName(column = "is_bullish_engulfing")
    @CsvBindByPosition(position = 12)
    private boolean isBullishEngulfing;

    @CsvBindByName(column = "is_bearish_engulfing")
    @CsvBindByPosition(position = 13)
    private boolean isBearishEngulfing;

    @CsvBindByName(column = "are_three_white_soldiers")
    @CsvBindByPosition(position = 14)
    private boolean areThreeWhiteSoldiers;

    @CsvBindByName(column = "are_three_black_crows")
    @CsvBindByPosition(position = 15)
    private boolean areThreeBlackCrows;

    @CsvBindByName(column = "is_doji")
    @CsvBindByPosition(position = 16)
    private boolean isDoji;

    public static CandleDtoRs ConvertToCandleDtoRs(Candle candle, String ticker) {
        return CandleDtoRs
                .builder()
                .ticker(ticker)
                .begin(candle.getDate())
                .open(candle.getOpen())
                .high(candle.getHigh())
                .low(candle.getLow())
                .close(candle.getClose())
                .volume(candle.getVolume())
                .rsi(candle.getIndicators().rsi())
                .macd(candle.getIndicators().macd())
                .cci(candle.getIndicators().cci())
                .ema9(candle.getIndicators().ema9())
                .ema50(candle.getIndicators().ema50())
                .isBullishEngulfing(candle.getPatterns().isBullishEngulfing())
                .isBearishEngulfing(candle.getPatterns().isBearishEngulfing())
                .areThreeWhiteSoldiers(candle.getPatterns().areThreeWhiteSoldiers())
                .areThreeBlackCrows(candle.getPatterns().areThreeBlackCrows())
                .isDoji(candle.getPatterns().isDoji())
                .build();
    }
}
