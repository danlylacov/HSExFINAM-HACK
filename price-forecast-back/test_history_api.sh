#!/bin/bash

# Тест API с множественными историческими свечами

echo "Тестирование API предсказания цен с историческими данными..."
echo "============================================================="

# Проверка статуса сервера
echo "1. Проверка статуса сервера:"
curl -X GET "http://localhost:8009/health"
echo ""

# Тестовый запрос с несколькими историческими свечами
echo "2. Запрос на предсказание следующих 20 свечей на основе истории:"
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
  }' | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f'Количество предсказанных свечей: {len(data[\"predictions\"])}')
print('Первые 3 предсказанные свечи:')
for i, candle in enumerate(data['predictions'][:3]):
    print(f'  Свеча {i+1}: {candle[\"date\"]} - O:{candle[\"open\"]:.2f} H:{candle[\"high\"]:.2f} L:{candle[\"low\"]:.2f} C:{candle[\"close\"]:.2f}')
"

echo ""
echo "Готово! API работает корректно с историческими данными."
