#!/usr/bin/env python3
"""
Простой тест для отладки эндпоинта
"""

import requests
import json

def simple_test():
    """Простой тест"""
    base_url = "http://localhost:8009"
    
    # Минимальные тестовые данные
    test_news_data = [
        {
            "date": "2025-01-01",
            "ticker": "AFLT",
            "nn_news_sum": 1.2
        }
    ]
    
    test_candle_data = [
        {
            "date": "2025-01-01",
            "ticker": "AFLT",
            "open": 100.0,
            "high": 105.0,
            "low": 95.0,
            "close": 102.0,
            "volume": 1000000
        }
    ]
    
    # Создаем запрос
    request_data = {
        "sessionId": "test_session_123",
        "newsData": json.dumps(test_news_data),
        "candleData": json.dumps(test_candle_data)
    }
    
    print("Простой тест эндпоинта...")
    
    try:
        response = requests.post(
            f"{base_url}/process-combined-data",
            json=request_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"Статус: {response.status_code}")
        print(f"Ответ: {response.text}")
        
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    simple_test()
