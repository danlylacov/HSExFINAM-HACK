package ru.viktorgezz.collector_of_all_data.service;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import ru.viktorgezz.collector_of_all_data.exception.SessionNotFoundException;
import ru.viktorgezz.collector_of_all_data.model.ProcessingSession;
import ru.viktorgezz.collector_of_all_data.model.ProcessingStatus;
import ru.viktorgezz.collector_of_all_data.repo.SessionRepository;

@Slf4j
@Service
@RequiredArgsConstructor
public class SessionService {

    private final SessionRepository sessionRepository;

    public ProcessingSession createSession() {
        ProcessingSession session = ProcessingSession.create();
        sessionRepository.save(session);
        log.info("Created new processing session: {}", session.getSessionId());
        return session;
    }

    public ProcessingSession getSession(String sessionId) {
        return sessionRepository.findById(sessionId)
                .orElseThrow(() -> new SessionNotFoundException("Session not found: " + sessionId));
    }

    public void updateNewsData(String sessionId, String newsData) {
        ProcessingSession session = getSession(sessionId);
        session.setNewsData(newsData);
        session.updateStatus(ProcessingStatus.NEWS_PROCESSING);
        sessionRepository.save(session);
        log.info("Updated news data for session: {}", sessionId);
    }

    public void updateCandleData(String sessionId, String candleData) {
        ProcessingSession session = getSession(sessionId);
        session.setCandleData(candleData);
        session.updateStatus(ProcessingStatus.CANDLE_PROCESSING);
        sessionRepository.save(session);
        log.info("Updated candle data for session: {}", sessionId);
    }

    public void markReadyForPrediction(String sessionId) {
        ProcessingSession session = getSession(sessionId);
        session.updateStatus(ProcessingStatus.READY_FOR_PREDICTION);
        sessionRepository.save(session);
        log.info("Session {} is ready for prediction", sessionId);
    }

    public void markPredictionInProgress(String sessionId) {
        ProcessingSession session = getSession(sessionId);
        session.updateStatus(ProcessingStatus.PREDICTION_IN_PROGRESS);
        sessionRepository.save(session);
        log.info("Prediction started for session: {}", sessionId);
    }

    public void completePrediction(String sessionId, String predictionResult) {
        ProcessingSession session = getSession(sessionId);
        session.setPredictionResult(predictionResult);
        session.updateStatus(ProcessingStatus.COMPLETED);
        sessionRepository.save(session);
        log.info("Completed prediction for session: {}", sessionId);
    }

    public void markFailed(String sessionId, String errorMessage) {
        ProcessingSession session = getSession(sessionId);
        session.setErrorMessage(errorMessage);
        session.updateStatus(ProcessingStatus.FAILED);
        sessionRepository.save(session);
        log.error("Session {} failed: {}", sessionId, errorMessage);
    }

    public void deleteSession(String sessionId) {
        sessionRepository.deleteById(sessionId);
        log.info("Deleted session: {}", sessionId);
    }
}
