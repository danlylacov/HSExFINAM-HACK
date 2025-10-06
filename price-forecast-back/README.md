# Price Prediction API

FastAPI бэкенд для предсказания цен на основе обученной модели из ноутбука.

## Установка и запуск

1. Установите зависимости:
```bash
pip3 install -r requirements.txt
```

2. Обучите и сохраните модели:
```bash
python3 train_models.py
```

3. Запустите API сервер:
```bash
python3 main.py
```

Сервер будет доступен по адресу: http://localhost:8009

## Тестирование

Для тестирования API используйте:
```bash
python3 test_api.py
```

## Использование API

### Эндпоинт: POST /predict

Принимает массив исторических свечей и возвращает предсказания следующих 20 свечей:

**Входной формат:**
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
        },
        {
            "ticker": "AFLT",
            "date": "2025-01-02",
            // ... еще исторические свечи
        }
    ]
}
```

**Ответ:**
```json
{
    "predictions": [
        {
            "date": "2025-01-04",
            "ticker": "AFLT",
            "open": 113.2,
            "high": 104.9,
            "low": 85.4,
            "close": 99.0,
            "volume": -141702
        },
    ]
}
```

**Логика работы:**
- API принимает массив исторических свечей
- Анализирует всю историю для создания признаков (лаговые, скользящие статистики, волатильность)
- Предсказывает следующие 20 свечей на основе всей истории
- Каждая новая свеча добавляется к истории для предсказания следующей

### Эндпоинты для обучения модели

#### `POST /upload-data`
Загрузка данных для обучения модели (CSV или JSON)

**Пример запроса:**
```bash
curl -X POST "http://localhost:8009/upload-data" \
  -F "file=@your_data.csv"
```

#### `POST /train`
Обучение модели с настраиваемыми параметрами

**Параметры:**
- `filename`: имя загруженного файла
- `config`: JSON конфигурация параметров обучения

**Пример запроса:**
```bash
curl -X POST "http://localhost:8009/train" \
  -F "filename=your_data.csv" \
  -F 'config={"train_size": 30, "rf_n_estimators": 100, "ensemble_weights": [2,2,1,1,1]}'
```

#### `GET /training-config`
Получение конфигурации по умолчанию для обучения

#### `GET /data-files`
Получение списка загруженных файлов с данными

### Другие эндпоинты

- `GET /` - информация о API
- `GET /health` - проверка состояния сервера и загруженных моделей

## Структура проекта

- `main.py` - основной файл FastAPI приложения
- `train_models.py` - скрипт для обучения и сохранения моделей
- `requirements.txt` - зависимости Python
- `models/` - папка с сохраненными моделями (создается автоматически)

## Модель

Используется ансамбль из 5 моделей:
- Random Forest
- Gradient Boosting
- Extra Trees
- Ridge Regression
- Lasso Regression

Модели обучены на признаках:
- Новостные данные (nn_news_*)
- Сентимент анализ (sentiment_*)
- Технические индикаторы (rsi, macd, cci, ema9, ema50)
- Свечные паттерны (areThreeWhiteSoldiers, etc.)
- Лаговые признаки и скользящие статистики