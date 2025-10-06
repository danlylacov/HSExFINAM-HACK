package ru.viktorgezz.market_analyzer_service.service.intrf;

import org.springframework.web.multipart.MultipartFile;
import ru.viktorgezz.market_analyzer_service.model.Candle;

import java.util.List;
import java.util.Map;

public interface ReceiveCandles {

    Map<String, List<Candle>> processCandlesByTicker(MultipartFile fileCandles);
}
