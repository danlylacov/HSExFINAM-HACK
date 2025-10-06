package ru.viktorgezz.market_analyzer_service.converter;

import org.springframework.web.multipart.MultipartFile;
import ru.viktorgezz.market_analyzer_service.dto.CandleDtoRs;

import java.util.List;

public interface ConverterCsv {

    List<CandleDtoRs> calculateIndicatorsAndPatterns(MultipartFile fileCandles);
}
