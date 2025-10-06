package ru.viktorgezz.market_analyzer_service.service.impl;

import com.opencsv.bean.CsvToBeanBuilder;
import lombok.SneakyThrows;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;
import ru.viktorgezz.market_analyzer_service.dto.CandleDtoRq;
import ru.viktorgezz.market_analyzer_service.model.Candle;
import ru.viktorgezz.market_analyzer_service.service.intrf.ReceiveCandles;

import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
public class ReceiveCandlesFromCsvImpl implements ReceiveCandles {

    @Override
    public Map<String, List<Candle>> processCandlesByTicker(MultipartFile fileCandles) {
        return getAllCandles(fileCandles).stream()
                .collect(Collectors.groupingBy(
                        CandleDtoRq::getTicker,
                        Collectors.mapping(
                                Candle::from,
                                Collectors.toList()
                        )
                ));
    }

    @SneakyThrows
    private List<CandleDtoRq> getAllCandles(MultipartFile fileCandles) {
        try (InputStreamReader reader = new InputStreamReader(fileCandles.getInputStream(), StandardCharsets.UTF_8)) {
            return new CsvToBeanBuilder<CandleDtoRq>(reader)
                    .withType(CandleDtoRq.class)
                    .build()
                    .parse()
                    .stream()
                    .distinct()
                    .collect(Collectors.toList());
        }
    }
}
