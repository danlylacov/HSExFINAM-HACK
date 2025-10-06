# Price Prediction API - Подробное руководство по обучению

## 📋 Содержание

1. [Обзор системы](#обзор-системы)
2. [Установка и настройка](#установка-и-настройка)
3. [Подготовка данных](#подготовка-данных)
4. [Обучение модели через API](#обучение-модели-через-api)
5. [Настройка параметров обучения](#настройка-параметров-обучения)
6. [Мониторинг и валидация](#мониторинг-и-валидация)
7. [Примеры использования](#примеры-использования)
8. [Устранение неполадок](#устранение-неполадок)

## 🎯 Обзор системы

API для предсказания цен акций использует ансамбль машинного обучения, состоящий из 5 алгоритмов:
- **Random Forest** - случайный лес
- **Gradient Boosting** - градиентный бустинг
- **Extra Trees** - экстра деревья
- **Ridge Regression** - ридж регрессия
- **Lasso Regression** - лассо регрессия

Система автоматически создает дополнительные признаки и обучает отдельные модели для каждой целевой переменной (open, high, low, close, volume).

## 🚀 Установка и настройка

### 1. Установка зависимостей

```bash
# Клонирование репозитория
git clone <repository-url>
cd row_price2

# Установка Python зависимостей
pip3 install -r requirements.txt
```

### 2. Запуск сервера

```bash
# Запуск API сервера
python3 main.py
```

Сервер будет доступен по адресу: http://localhost:8009

### 3. Проверка работоспособности

```bash
# Проверка статуса
curl -X GET "http://localhost:8009/health"
```

## 📊 Подготовка данных

### Формат данных

API принимает данные в форматах CSV или JSON. Обязательные поля:

#### Основные поля:
- `ticker` - тикер акции (строка)
- `date` или `begin` - дата (YYYY-MM-DD)
- `open`, `high`, `low`, `close` - цены OHLC
- `volume` - объем торгов

#### Новостные данные:
- `nn_news_sum` - сумма новостных метрик
- `nn_news_mean` - среднее новостных метрик
- `nn_news_max` - максимум новостных метрик
- `nn_news_count` - количество новостей

#### Сентимент анализ:
- `sentiment_mean` - средний сентимент
- `sentiment_sum` - сумма сентиментов
- `sentiment_count` - количество сентиментов
- `sentiment_positive_count` - количество позитивных
- `sentiment_negative_count` - количество негативных
- `sentiment_neutral_count` - количество нейтральных

#### Технические индикаторы:
- `rsi` - индекс относительной силы
- `macd` - MACD индикатор
- `cci` - Commodity Channel Index
- `ema9` - экспоненциальная скользящая средняя (9)
- `ema50` - экспоненциальная скользящая средняя (50)

#### Свечные паттерны:
- `areThreeWhiteSoldiers` - три белых солдата
- `areThreeBlackCrows` - три черных ворона
- `doji` - доджи
- `bearishEngulfing` - медвежий поглощающий
- `bullishEngulfing` - бычий поглощающий

### Пример CSV файла:

```csv
ticker,begin,nn_news_sum,nn_news_mean,nn_news_max,nn_news_count,sentiment_mean,sentiment_sum,sentiment_count,sentiment_positive_count,sentiment_negative_count,sentiment_neutral_count,rsi,macd,cci,ema9,ema50,areThreeWhiteSoldiers,areThreeBlackCrows,doji,bearishEngulfing,bullishEngulfing,open,high,low,close,volume
AFLT,2025-01-01,1.2,0.03,0.18,43,0.5,20.0,40,20,10,10,50.0,0.5,0.0,100.0,100.0,0,0,0,0,0,100.0,105.0,95.0,102.0,1000000
AFLT,2025-01-02,1.1,0.025,0.15,44,0.6,26.4,44,25,8,11,55.0,0.6,5.0,101.0,100.5,0,0,0,0,0,102.0,108.0,98.0,105.0,1200000
```

## 🎓 Обучение модели через API

### Шаг 1: Загрузка данных

```bash
# Загрузка CSV файла
curl -X POST "http://localhost:8009/upload-data" \
  -F "file=@your_data.csv"

# Загрузка JSON файла
curl -X POST "http://localhost:8009/upload-data" \
  -F "file=@your_data.json"
```

**Ответ:**
```json
{
  "status": "success",
  "message": "Файл your_data.csv успешно загружен",
  "filename": "your_data.csv",
  "rows_count": 100,
  "columns_count": 27,
  "columns": ["ticker", "begin", "nn_news_sum", ...]
}
```

### Шаг 2: Получение конфигурации по умолчанию

```bash
curl -X GET "http://localhost:8009/training-config"
```

**Ответ:**
```json
{
  "default_config": {
    "train_size": 25,
    "test_size": null,
    "rf_n_estimators": 200,
    "rf_max_depth": 15,
    "rf_min_samples_split": 5,
    "rf_min_samples_leaf": 2,
    "gb_n_estimators": 200,
    "gb_learning_rate": 0.1,
    "gb_max_depth": 6,
    "gb_min_samples_split": 5,
    "et_n_estimators": 150,
    "et_max_depth": 15,
    "et_min_samples_split": 5,
    "ridge_alpha": 1.0,
    "lasso_alpha": 0.1,
    "lasso_max_iter": 2000,
    "ensemble_weights": [3, 3, 2, 1, 1],
    "cv_splits": 5,
    "feature_selection_threshold": "median",
    "feature_selection_n_estimators": 50
  },
  "description": {
    "train_size": "Количество записей для обучения",
    "test_size": "Количество записей для тестирования (None = все остальные)",
    "rf_n_estimators": "Количество деревьев в Random Forest",
    "rf_max_depth": "Максимальная глубина деревьев в Random Forest",
    "gb_n_estimators": "Количество деревьев в Gradient Boosting",
    "gb_learning_rate": "Скорость обучения в Gradient Boosting",
    "ensemble_weights": "Веса для ансамбля [RF, GB, ET, Ridge, Lasso]",
    "cv_splits": "Количество фолдов для кросс-валидации"
  }
}
```

### Шаг 3: Обучение модели

```bash
# Обучение с параметрами по умолчанию
curl -X POST "http://localhost:8009/train" \
  -F "filename=your_data.csv" \
  -F 'config={}'

# Обучение с кастомными параметрами
curl -X POST "http://localhost:8009/train" \
  -F "filename=your_data.csv" \
  -F 'config={"train_size": 50, "rf_n_estimators": 100, "ensemble_weights": [2,2,1,1,1]}'
```

**Ответ:**
```json
{
  "status": "success",
  "message": "Обучено 5 моделей",
  "models_trained": ["open", "high", "low", "close", "volume"],
  "training_metrics": {
    "open": {
      "cv_mae_mean": 9.5741,
      "cv_mae_std": 2.1974,
      "selected_features": 25,
      "total_features": 50
    },
    "high": {
      "cv_mae_mean": 8.9068,
      "cv_mae_std": 2.1640,
      "selected_features": 25,
      "total_features": 50
    },
    "low": {
      "cv_mae_mean": 8.6359,
      "cv_mae_std": 3.2213,
      "selected_features": 25,
      "total_features": 50
    },
    "close": {
      "cv_mae_mean": 8.1611,
      "cv_mae_std": 1.1316,
      "selected_features": 25,
      "total_features": 50
    },
    "volume": {
      "cv_mae_mean": 350541.6966,
      "cv_mae_std": 86300.5552,
      "selected_features": 25,
      "total_features": 50
    }
  },
  "feature_count": 50,
  "selected_features_count": 25
}
```

## ⚙️ Настройка параметров обучения

### Параметры разделения данных

```json
{
  "train_size": 30,        // Количество записей для обучения
  "test_size": 20         // Количество записей для тестирования (null = все остальные)
}
```

### Параметры Random Forest

```json
{
  "rf_n_estimators": 200,      // Количество деревьев
  "rf_max_depth": 15,          // Максимальная глубина
  "rf_min_samples_split": 5,   // Минимум образцов для разделения
  "rf_min_samples_leaf": 2     // Минимум образцов в листе
}
```

### Параметры Gradient Boosting

```json
{
  "gb_n_estimators": 200,      // Количество деревьев
  "gb_learning_rate": 0.1,    // Скорость обучения
  "gb_max_depth": 6,           // Максимальная глубина
  "gb_min_samples_split": 5    // Минимум образцов для разделения
}
```

### Параметры Extra Trees

```json
{
  "et_n_estimators": 150,      // Количество деревьев
  "et_max_depth": 15,          // Максимальная глубина
  "et_min_samples_split": 5    // Минимум образцов для разделения
}
```

### Параметры линейных моделей

```json
{
  "ridge_alpha": 1.0,          // Регуляризация Ridge
  "lasso_alpha": 0.1,          // Регуляризация Lasso
  "lasso_max_iter": 2000       // Максимум итераций для Lasso
}
```

### Веса ансамбля

```json
{
  "ensemble_weights": [3, 3, 2, 1, 1]  // [RF, GB, ET, Ridge, Lasso]
}
```

### Параметры валидации

```json
{
  "cv_splits": 5,                        // Количество фолдов кросс-валидации
  "feature_selection_threshold": "median", // Порог отбора признаков
  "feature_selection_n_estimators": 50    // Деревья для отбора признаков
}
```

## 📈 Мониторинг и валидация

### Метрики качества

После обучения вы получаете следующие метрики:

- **CV MAE Mean** - средняя абсолютная ошибка на кросс-валидации
- **CV MAE Std** - стандартное отклонение ошибки
- **Selected Features** - количество отобранных признаков
- **Total Features** - общее количество признаков

### Интерпретация метрик

- **Низкий CV MAE** - модель хорошо предсказывает
- **Низкое CV MAE Std** - стабильные предсказания
- **Высокий Selected Features** - модель использует много признаков

### Проверка статуса

```bash
# Проверка загруженных моделей
curl -X GET "http://localhost:8009/health"
```

**Ответ:**
```json
{
  "status": "healthy",
  "models_loaded": 5,
  "available_targets": ["open", "high", "low", "close", "volume"]
}
```

## 💡 Примеры использования

### Пример 1: Быстрое обучение

```bash
#!/bin/bash

# 1. Загрузка данных
curl -X POST "http://localhost:8009/upload-data" \
  -F "file=@stock_data.csv"

# 2. Обучение с параметрами по умолчанию
curl -X POST "http://localhost:8009/train" \
  -F "filename=stock_data.csv" \
  -F 'config={}'

# 3. Проверка статуса
curl -X GET "http://localhost:8009/health"
```

### Пример 2: Тонкая настройка

```bash
#!/bin/bash

# Конфигурация для точной настройки
CONFIG='{
  "train_size": 100,
  "test_size": 50,
  "rf_n_estimators": 500,
  "rf_max_depth": 20,
  "gb_n_estimators": 300,
  "gb_learning_rate": 0.05,
  "ensemble_weights": [4, 4, 2, 1, 1],
  "cv_splits": 10
}'

# Обучение с тонкой настройкой
curl -X POST "http://localhost:8009/train" \
  -F "filename=stock_data.csv" \
  -F "config=$CONFIG"
```

### Пример 3: Экспериментальное обучение

```bash
#!/bin/bash

# Различные конфигурации для экспериментов
configs=(
  '{"train_size": 30, "rf_n_estimators": 50, "ensemble_weights": [1,1,1,1,1]}'
  '{"train_size": 50, "rf_n_estimators": 100, "ensemble_weights": [2,2,1,1,1]}'
  '{"train_size": 80, "rf_n_estimators": 200, "ensemble_weights": [3,3,2,1,1]}'
)

for i in "${!configs[@]}"; do
  echo "Эксперимент $((i+1)):"
  curl -X POST "http://localhost:8009/train" \
    -F "filename=stock_data.csv" \
    -F "config=${configs[$i]}"
  echo ""
done
```

## 🔧 Устранение неполадок

### Проблема: "Файл не найден"

**Решение:**
```bash
# Проверьте список загруженных файлов
curl -X GET "http://localhost:8009/data-files"

# Убедитесь, что файл загружен правильно
curl -X POST "http://localhost:8009/upload-data" \
  -F "file=@your_data.csv"
```

### Проблема: "Неверный формат JSON конфигурации"

**Решение:**
```bash
# Проверьте JSON синтаксис
echo '{"train_size": 30}' | python3 -m json.tool

# Используйте экранирование в bash
curl -X POST "http://localhost:8009/train" \
  -F "filename=data.csv" \
  -F 'config={"train_size": 30}'
```

### Проблема: "Модели не загружены"

**Решение:**
```bash
# Перезапустите сервер
pkill -f "python3 main.py"
python3 main.py

# Или переобучите модели
curl -X POST "http://localhost:8009/train" \
  -F "filename=data.csv" \
  -F 'config={}'
```

### Проблема: Низкое качество предсказаний

**Решения:**
1. **Увеличьте размер обучающей выборки:**
   ```json
   {"train_size": 100}
   ```

2. **Увеличьте количество деревьев:**
   ```json
   {"rf_n_estimators": 500, "gb_n_estimators": 300}
   ```

3. **Настройте веса ансамбля:**
   ```json
   {"ensemble_weights": [4, 4, 2, 1, 1]}
   ```

4. **Увеличьте количество фолдов валидации:**
   ```json
   {"cv_splits": 10}
   ```

## 📚 Дополнительные ресурсы

### Полезные команды

```bash
# Получение списка всех файлов
curl -X GET "http://localhost:8009/data-files"

# Получение документации API
curl -X GET "http://localhost:8009/docs"

# Получение OpenAPI схемы
curl -X GET "http://localhost:8009/openapi.json"
```

### Логирование

Все операции обучения логируются в консоль сервера. Следите за сообщениями:
- `"Обучение модели для {target}..."`
- `"Модель для {target} обучена. CV MAE: {score}"`
- `"Загружено {count} моделей"`

### Рекомендации по производительности

1. **Для быстрого прототипирования:**
   ```json
   {
     "train_size": 30,
     "rf_n_estimators": 50,
     "gb_n_estimators": 50,
     "cv_splits": 3
   }
   ```

2. **Для продакшена:**
   ```json
   {
     "train_size": 200,
     "rf_n_estimators": 500,
     "gb_n_estimators": 300,
     "cv_splits": 10
   }
   ```

3. **Для экспериментов:**
   ```json
   {
     "train_size": 100,
     "rf_n_estimators": 200,
     "gb_n_estimators": 200,
     "cv_splits": 5
   }
   ```

---

**Удачного обучения! 🚀**
