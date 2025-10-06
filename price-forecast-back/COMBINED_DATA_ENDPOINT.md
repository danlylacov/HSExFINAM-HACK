# Эндпоинт обработки комбинированных данных

## Описание

Новый эндпоинт `/process-combined-data` предназначен для объединения новостных данных и данных свечей по дате и тикеру.

## Входной формат

```json
{
  "sessionId": "session_123",
  "newsData": "[{\"date\": \"2025-01-01\", \"ticker\": \"AFLT\", \"nn_news_sum\": 1.2, ...}]",
  "candleData": "[{\"date\": \"2025-01-01\", \"ticker\": \"AFLT\", \"open\": 100.0, ...}]"
}
```

### Поля запроса:
- `sessionId` (string) - идентификатор сессии
- `newsData` (string) - JSON строка с массивом новостных данных
- `candleData` (string) - JSON строка с массивом данных свечей

### Структура новостных данных:
```json
{
  "date": "2025-01-01",
  "ticker": "AFLT",
  "nn_news_sum": 1.2,
  "nn_news_mean": 0.03,
  "nn_news_max": 0.18,
  "nn_news_count": 43,
  "sentiment_mean": 0.5,
  "sentiment_sum": 20.0,
  "sentiment_count": 40,
  "sentiment_positive_count": 20,
  "sentiment_negative_count": 10,
  "sentiment_neutral_count": 10
}
```

### Структура данных свечей:
```json
{
  "date": "2025-01-01",
  "ticker": "AFLT",
  "open": 100.0,
  "high": 105.0,
  "low": 95.0,
  "close": 102.0,
  "volume": 1000000,
  "rsi": 50.0,
  "macd": 0.5,
  "cci": 0.0,
  "ema9": 100.0,
  "ema50": 100.0,
  "areThreeWhiteSoldiers": 0,
  "areThreeBlackCrows": 0,
  "doji": 0,
  "bearishEngulfing": 0,
  "bullishEngulfing": 0
}
```

## Выходной формат

```json
{
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
```

## Логика работы

1. **Парсинг данных**: JSON строки преобразуются в массивы объектов
2. **Объединение по ключам**: Для каждой свечи ищутся соответствующие новости по дате и тикеру
3. **Объединение данных**: 
   - Если новости найдены - объединяются все поля
   - Если новости не найдены - новостные поля устанавливаются в 0
4. **Заполнение недостающих полей**: Технические индикаторы заполняются значениями по умолчанию
5. **Сериализация**: numpy типы преобразуются в обычные Python типы

## Пример использования

```bash
curl -X POST "http://localhost:8009/process-combined-data" \
  -H "Content-Type: application/json" \
  -d '{
    "sessionId": "test_session_123",
    "newsData": "[{\"date\": \"2025-01-01\", \"ticker\": \"AFLT\", \"nn_news_sum\": 1.2}]",
    "candleData": "[{\"date\": \"2025-01-01\", \"ticker\": \"AFLT\", \"open\": 100.0, \"high\": 105.0, \"low\": 95.0, \"close\": 102.0, \"volume\": 1000000}]"
  }'
```

## Обработка ошибок

- **400 Bad Request**: Ошибка парсинга JSON
- **500 Internal Server Error**: Ошибка обработки данных

## Тестирование

Для тестирования используйте файл `test_combined_data_fixed.py`:

```bash
python3 test_combined_data_fixed.py
```

Тест проверяет:
- Корректность объединения данных
- Правильность установки значений по умолчанию
- Логику поиска новостей по дате и тикеру
