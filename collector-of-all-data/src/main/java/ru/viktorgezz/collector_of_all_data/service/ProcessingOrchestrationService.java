package ru.viktorgezz.collector_of_all_data.service;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;
import ru.viktorgezz.collector_of_all_data.model.ProcessingSession;

/**
 * Сервис-оркестратор, координирующий процесс обработки файлов
**/
@Slf4j
@Service
@RequiredArgsConstructor
public class ProcessingOrchestrationService {

    private final SessionService sessionService;
    private final DataProcessingService dataProcessingService;

    /**
     * Инициирует обработку файлов
     *
     * @param newsFile файл с новостями
     * @param candleFile файл со свечами
     * @return идентификатор сессии обработки
     */
    public String initiateProcessing(MultipartFile newsFile, MultipartFile candleFile) {
        log.info("Initiating new processing for files: {} and {}",
                newsFile.getOriginalFilename(), candleFile.getOriginalFilename());

        // Создаем новую сессию обработки
        ProcessingSession session = sessionService.createSession();
        String sessionId = session.getSessionId();

        try {
            // Параллельно отправляем оба файла на обработку
            dataProcessingService.processCandleFile(candleFile, sessionId);
            dataProcessingService.processNewsFile(newsFile, sessionId);

            log.info("Processing initiated successfully for session: {}", sessionId);

        } catch (Exception e) {
            log.error("Error initiating processing for session: {}", sessionId, e);
            sessionService.markFailed(sessionId, "Failed to initiate processing: " + e.getMessage());
            throw new RuntimeException("Failed to initiate processing", e);
        }

        return sessionId;
    }
}
