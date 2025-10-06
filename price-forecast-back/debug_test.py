import json

# Простой тест без requests
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

# Импортируем функции из main.py для прямого тестирования
import sys
sys.path.append('.')

try:
    from main import predict_single_candle, generate_20_candles, load_models
    
    print("Загружаем модели...")
    load_models()
    
    print("Тестирование predict_single_candle...")
    result = predict_single_candle(test_data["params"][0])
    print(f"Результат: {result}")
    
    print("\nТестирование generate_20_candles...")
    candles = generate_20_candles(test_data["params"][0])
    print(f"Количество свечей: {len(candles)}")
    print(f"Первая свеча: {candles[0]}")
    
except Exception as e:
    import traceback
    print(f"Ошибка: {e}")
    print(f"Traceback: {traceback.format_exc()}")
