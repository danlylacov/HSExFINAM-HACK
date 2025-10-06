import requests
import json

# Тестовые данные
test_data = {
    "params": [
        {
            "ticker": "AFLT",
            "date": "2025-01-01",
            "nn_news_sum": 1.2,
            "nn_news_mean": 0.03,
            "nn_news_max": 0.18,
            "nn_news_count": 43,
            "sentiment_mean": 0.5,
            "sentiment_sum": 20.0,
            "sentiment_count": 40,
            "sentiment_positive_count": 20,
            "sentiment_negative_count": 10,
            "sentiment_neutral_count": 10,
            "rsi": 50.0,
            "macd": 0.5,
            "cci": 0.0,
            "ema9": 100.0,
            "ema50": 100.0,
            "areThreeWhiteSoldiers": 0,
            "areThreeBlackCrows": 0,
            "doji": 0,
            "bearishEngulfing": 0,
            "bullishEngulfing": 0,
            "open": 100.0,
            "high": 105.0,
            "low": 95.0,
            "close": 102.0,
            "volume": 1000000
        }
    ]
}

# Проверяем статус сервера
print("Проверка статуса сервера...")
try:
    response = requests.get("http://localhost:8009/health")
    print(f"Статус: {response.status_code}")
    print(f"Ответ: {response.json()}")
except Exception as e:
    print(f"Ошибка подключения: {e}")

print("\n" + "="*50 + "\n")

# Тестируем предсказание
print("Тестирование предсказания...")
try:
    response = requests.post(
        "http://localhost:8009/predict",
        headers={"Content-Type": "application/json"},
        json=test_data
    )
    
    print(f"Статус: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Количество предсказанных свечей: {len(result['predictions'])}")
        print("\nПервые 3 свечи:")
        for i, candle in enumerate(result['predictions'][:3]):
            print(f"Свеча {i+1}: {candle}")
    else:
        print(f"Ошибка: {response.text}")
        
except Exception as e:
    print(f"Ошибка запроса: {e}")
