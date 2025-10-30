package ru.viktorgezz.collector_of_all_data.controller;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.tags.Tag;
import io.swagger.v3.oas.annotations.Parameter;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import ru.viktorgezz.collector_of_all_data.service.ProcessingOrchestrationService;

import java.util.Map;

@Slf4j
@RestController
@RequestMapping("/api/v1/processing")
@RequiredArgsConstructor
@Tag(name = "Загрузка файлов", description = "Эндпоинты для загрузки CSV-файлов с новостями и свечами")
public class FileUploadController {

    private final ProcessingOrchestrationService orchestrationService;

    @Operation(
            summary = "Загрузить файлы новостей и свечей",
            description = "Принимает два CSV-файла: новости и свечи. После загрузки инициирует процесс обработки и возвращает `sessionId` для отслеживания статуса.",
            responses = {
                    @ApiResponse(responseCode = "202", description = "Файлы приняты и обработка начата"),
                    @ApiResponse(responseCode = "400", description = "Ошибка валидации файлов", content = @Content)
            }
    )
    @PostMapping(value = "/upload", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ResponseEntity<Map<String, String>> uploadFiles(
            @Parameter(description = "CSV-файл с новостями", required = true)
            @RequestPart("newsFile") MultipartFile newsFile,

            @Parameter(description = "CSV-файл с данными свечей", required = true)
            @RequestPart("candleFile") MultipartFile candleFile
    ) {

        log.info("Received file upload request: newsFile={}, candleFile={}",
                newsFile.getOriginalFilename(), candleFile.getOriginalFilename());

        validateFiles(newsFile, candleFile);

        String sessionId = orchestrationService.initiateProcessing(newsFile, candleFile);

        return ResponseEntity.accepted()
                .body(Map.of(
                        "sessionId", sessionId,
                        "message", "Files received and processing initiated. Use sessionId to check status."
                ));
    }

    private void validateFiles(MultipartFile newsFile, MultipartFile candleFile) {
        if (newsFile.isEmpty()) {
            throw new IllegalArgumentException("News file is empty");
        }
        if (candleFile.isEmpty()) {
            throw new IllegalArgumentException("Candle file is empty");
        }
        if (!newsFile.getOriginalFilename().endsWith(".csv")) {
            throw new IllegalArgumentException("News file must be a CSV");
        }
        if (!candleFile.getOriginalFilename().endsWith(".csv")) {
            throw new IllegalArgumentException("Candle file must be a CSV");
        }
    }
}
