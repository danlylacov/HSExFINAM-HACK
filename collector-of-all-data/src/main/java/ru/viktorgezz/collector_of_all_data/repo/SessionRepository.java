package ru.viktorgezz.collector_of_all_data.repo;

import org.springframework.stereotype.Repository;
import ru.viktorgezz.collector_of_all_data.model.ProcessingSession;

import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;

@Repository
public class SessionRepository {

    private final Map<String, ProcessingSession> sessions = new ConcurrentHashMap<>();

    public ProcessingSession save(ProcessingSession session) {
        sessions.put(session.getSessionId(), session);
        return session;
    }

    public Optional<ProcessingSession> findById(String sessionId) {
        return Optional.ofNullable(sessions.get(sessionId));
    }

    public void deleteById(String sessionId) {
        sessions.remove(sessionId);
    }

    public boolean exists(String sessionId) {
        return sessions.containsKey(sessionId);
    }
}
