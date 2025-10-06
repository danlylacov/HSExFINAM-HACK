package ru.viktorgezz.market_analyzer_service.dto;

import com.opencsv.bean.CsvBindByName;
import com.opencsv.bean.CsvDate;
import lombok.Data;

import java.time.LocalDate;
import java.util.Objects;

@Data
public class CandleDtoRq {

    @CsvBindByName(column = "open", required = true)
    private double open;

    @CsvBindByName(column = "close", required = true)
    private double close;

    @CsvBindByName(column = "high", required = true)
    private double high;

    @CsvBindByName(column = "low", required = true)
    private double low;

    @CsvBindByName(column = "volume", required = true)
    private long volume;

    @CsvBindByName(column = "begin", required = true)
    @CsvDate("yyyy-MM-dd")
    private LocalDate begin;

    @CsvBindByName(column = "ticker", required = true)
    private String ticker;

    @Override
    public boolean equals(Object object) {
        if (this == object) return true;
        if (object == null || getClass() != object.getClass()) return false;
        CandleDtoRq that = (CandleDtoRq) object;
        return volume == that.volume && Objects.equals(begin, that.begin) && Objects.equals(ticker, that.ticker);
    }

    @Override
    public int hashCode() {
        return Objects.hash(volume, begin, ticker);
    }
}
