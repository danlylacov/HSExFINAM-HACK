package ru.viktorgezz.collector_of_all_data.client;

import org.springframework.web.multipart.MultipartFile;

public interface ExternalServiceClient {

    /**
     * Отправляет файл на внешний сервис с указанием URL для callback
     *
     * @param file файл для обработки
     * @param serviceUrl URL внешнего сервиса
     * @param callbackUrl URL для обратного вызова
     * @param sessionId идентификатор сессии обработки
     */
    void sendFileWithCallback(MultipartFile file, String serviceUrl, String callbackUrl, String sessionId);

    /**
     * Отправляет JSON данные на внешний сервис с указанием URL для callback
     *
     * @param jsonData JSON данные для обработки
     * @param serviceUrl URL внешнего сервиса
     * @param callbackUrl URL для обратного вызова
     * @param sessionId идентификатор сессии обработки
     */
    void sendJsonWithCallback(String jsonData, String serviceUrl, String callbackUrl, String sessionId);
}
