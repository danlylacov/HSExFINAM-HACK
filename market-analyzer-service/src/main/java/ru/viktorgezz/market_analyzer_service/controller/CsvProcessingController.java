package ru.viktorgezz.market_analyzer_service.controller;

import lombok.RequiredArgsConstructor;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;
import ru.viktorgezz.market_analyzer_service.client.ClientCallback;


@RestController
@RequiredArgsConstructor
public class CsvProcessingController {

    private final ClientCallback clientCallback;

    @PostMapping(value = "/candle", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public void processCandleCsvFiles(
            @RequestParam("file") MultipartFile fileCandles,
            @RequestParam("callbackUrl") String callbackUrl,
            @RequestParam("sessionId") String sessionId
    ) {
        clientCallback.send(callbackUrl, sessionId, fileCandles);
    }
}
