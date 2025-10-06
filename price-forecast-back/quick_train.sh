#!/bin/bash

# Скрипт быстрого старта для обучения модели
# Использование: ./quick_train.sh <файл_с_данными>

if [ $# -eq 0 ]; then
    echo "Использование: $0 <файл_с_данными.csv>"
    echo "Пример: $0 stock_data.csv"
    exit 1
fi

DATA_FILE=$1
BASE_URL="http://localhost:8009"

echo "=== Быстрый старт обучения модели ==="
echo "Файл данных: $DATA_FILE"
echo ""

# Проверка существования файла
if [ ! -f "$DATA_FILE" ]; then
    echo "❌ Ошибка: Файл $DATA_FILE не найден"
    exit 1
fi

# Проверка статуса сервера
echo "1. Проверка статуса сервера..."
if ! curl -s -f "$BASE_URL/health" > /dev/null; then
    echo "❌ Ошибка: Сервер не запущен. Запустите: python3 main.py"
    exit 1
fi
echo "✅ Сервер работает"

# Загрузка данных
echo ""
echo "2. Загрузка данных..."
UPLOAD_RESPONSE=$(curl -s -X POST "$BASE_URL/upload-data" -F "file=@$DATA_FILE")

if echo "$UPLOAD_RESPONSE" | grep -q '"status":"success"'; then
    FILENAME=$(echo "$UPLOAD_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['filename'])")
    ROWS=$(echo "$UPLOAD_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['rows_count'])")
    echo "✅ Файл загружен: $FILENAME ($ROWS строк)"
else
    echo "❌ Ошибка загрузки файла"
    echo "$UPLOAD_RESPONSE"
    exit 1
fi

# Выбор конфигурации обучения
echo ""
echo "3. Выбор конфигурации обучения..."
echo "Выберите режим обучения:"
echo "1) Быстрое обучение (30 записей, 50 деревьев)"
echo "2) Стандартное обучение (50 записей, 100 деревьев)"
echo "3) Точное обучение (100 записей, 200 деревьев)"
echo "4) Кастомная конфигурация"

read -p "Введите номер (1-4): " choice

case $choice in
    1)
        CONFIG='{"train_size": 30, "rf_n_estimators": 50, "gb_n_estimators": 50, "cv_splits": 3}'
        echo "Выбрано: Быстрое обучение"
        ;;
    2)
        CONFIG='{"train_size": 50, "rf_n_estimators": 100, "gb_n_estimators": 100, "cv_splits": 5}'
        echo "Выбрано: Стандартное обучение"
        ;;
    3)
        CONFIG='{"train_size": 100, "rf_n_estimators": 200, "gb_n_estimators": 200, "cv_splits": 5}'
        echo "Выбрано: Точное обучение"
        ;;
    4)
        echo "Введите кастомную конфигурацию (JSON):"
        read CONFIG
        ;;
    *)
        echo "❌ Неверный выбор"
        exit 1
        ;;
esac

# Обучение модели
echo ""
echo "4. Обучение модели..."
echo "Конфигурация: $CONFIG"
echo "Обучение может занять несколько минут..."

TRAIN_RESPONSE=$(curl -s -X POST "$BASE_URL/train" -F "filename=$FILENAME" -F "config=$CONFIG")

if echo "$TRAIN_RESPONSE" | grep -q '"status":"success"'; then
    echo "✅ Обучение завершено успешно!"
    
    # Парсинг результатов
    MODELS=$(echo "$TRAIN_RESPONSE" | python3 -c "import sys, json; print(', '.join(json.load(sys.stdin)['models_trained']))")
    FEATURES=$(echo "$TRAIN_RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(f\"{data['feature_count']} -> {data['selected_features_count']}\")")
    
    echo ""
    echo "📊 Результаты обучения:"
    echo "   Обученные модели: $MODELS"
    echo "   Признаки: $FEATURES"
    
    echo ""
    echo "📈 Метрики качества:"
    echo "$TRAIN_RESPONSE" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for target, metrics in data['training_metrics'].items():
    print(f'   {target}: CV MAE = {metrics[\"cv_mae_mean\"]:.4f} (+/- {metrics[\"cv_mae_std\"]:.4f})')
"
else
    echo "❌ Ошибка обучения"
    echo "$TRAIN_RESPONSE"
    exit 1
fi

# Проверка финального статуса
echo ""
echo "5. Проверка финального статуса..."
HEALTH_RESPONSE=$(curl -s "$BASE_URL/health")
MODELS_LOADED=$(echo "$HEALTH_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['models_loaded'])")

echo "✅ Загружено моделей: $MODELS_LOADED"

# Тестовое предсказание
echo ""
echo "6. Тестовое предсказание..."
TEST_DATA='{
  "params": [
    {
      "ticker": "TEST",
      "date": "2025-01-01",
      "nn_news_sum": 1.0,
      "nn_news_mean": 0.02,
      "nn_news_max": 0.15,
      "nn_news_count": 40,
      "sentiment_mean": 0.5,
      "sentiment_sum": 20.0,
      "sentiment_count": 40,
      "sentiment_positive_count": 20,
      "sentiment_negative_count": 10,
      "sentiment_neutral_count": 10,
      "rsi": 50.0,
      "macd": 0.0,
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
}'

PREDICT_RESPONSE=$(curl -s -X POST "$BASE_URL/predict" \
  -H "Content-Type: application/json" \
  -d "$TEST_DATA")

if echo "$PREDICT_RESPONSE" | grep -q '"predictions"'; then
    PREDICTIONS_COUNT=$(echo "$PREDICT_RESPONSE" | python3 -c "import sys, json; print(len(json.load(sys.stdin)['predictions']))")
    echo "✅ Тестовое предсказание: $PREDICTIONS_COUNT свечей"
else
    echo "❌ Ошибка тестового предсказания"
fi

echo ""
echo "🎉 Обучение завершено успешно!"
echo ""
echo "📋 Следующие шаги:"
echo "   1. Используйте /predict для получения предсказаний"
echo "   2. Проверьте /health для статуса системы"
echo "   3. Используйте /docs для документации API"
echo ""
echo "🔗 Полезные ссылки:"
echo "   - API документация: http://localhost:8009/docs"
echo "   - Статус системы: http://localhost:8009/health"
echo "   - Список файлов: http://localhost:8009/data-files"
