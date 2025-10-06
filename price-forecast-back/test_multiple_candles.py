import requests
import json

# Тестовые данные - несколько исторических свечей
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
        },
        {
            "ticker": "AFLT",
            "date": "2025-01-02",
            "nn_news_sum": 1.1,
            "nn_news_mean": 0.025,
            "nn_news_max": 0.15,
            "nn_news_count": 44,
            "sentiment_mean": 0.6,
            "sentiment_sum": 26.4,
            "sentiment_count": 44,
            "sentiment_positive_count": 25,
            "sentiment_negative_count": 8,
            "sentiment_neutral_count": 11,
            "rsi": 55.0,
            "macd": 0.6,
            "cci": 5.0,
            "ema9": 101.0,
            "ema50": 100.5,
            "areThreeWhiteSoldiers": 0,
            "areThreeBlackCrows": 0,
            "doji": 0,
            "bearishEngulfing": 0,
            "bullishEngulfing": 0,
            "open": 102.0,
            "high": 108.0,
            "low": 98.0,
            "close": 105.0,
            "volume": 1200000
        },
        {
            "ticker": "AFLT",
            "date": "2025-01-03",
            "nn_news_sum": 0.9,
            "nn_news_mean": 0.02,
            "nn_news_max": 0.12,
            "nn_news_count": 45,
            "sentiment_mean": 0.4,
            "sentiment_sum": 18.0,
            "sentiment_count": 45,
            "sentiment_positive_count": 15,
            "sentiment_negative_count": 20,
            "sentiment_neutral_count": 10,
            "rsi": 45.0,
            "macd": 0.3,
            "cci": -10.0,
            "ema9": 99.5,
            "ema50": 100.2,
            "areThreeWhiteSoldiers": 0,
            "areThreeBlackCrows": 0,
            "doji": 0,
            "bearishEngulfing": 0,
            "bullishEngulfing": 0,
            "open": 105.0,
            "high": 107.0,
            "low": 100.0,
            "close": 103.0,
            "volume": 1100000
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
print("Тестирование предсказания следующих 20 свечей на основе истории...")
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
        print("\nПервые 5 предсказанных свечей:")
        for i, candle in enumerate(result['predictions'][:5]):
            print(f"Свеча {i+1}: {candle}")
    else:
        print(f"Ошибка: {response.text}")
        
except Exception as e:
    print(f"Ошибка запроса: {e}")
