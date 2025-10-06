#!/bin/bash

# Пример использования API для предсказания цен

echo "Тестирование API предсказания цен..."
echo "=================================="

# Проверка статуса сервера
echo "1. Проверка статуса сервера:"
curl -X GET "http://localhost:8009/health" | jq .
echo ""

# Тестовый запрос на предсказание
echo "2. Запрос на предсказание 20 свечей:"
curl -X POST "http://localhost:8009/predict" \
  -H "Content-Type: application/json" \
  -d '{
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
  }' | jq '.predictions | length'

echo ""
echo "Готово! API работает корректно."
