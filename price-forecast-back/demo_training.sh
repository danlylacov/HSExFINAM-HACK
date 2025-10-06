#!/bin/bash

# Демонстрация новых эндпоинтов для обучения модели

echo "=== Демонстрация эндпоинтов обучения модели ==="
echo ""

# 1. Получение конфигурации по умолчанию
echo "1. Получение конфигурации по умолчанию:"
curl -X GET "http://localhost:8009/training-config" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f'   Статус: 200')
print(f'   Размер обучающей выборки: {data[\"default_config\"][\"train_size\"]}')
print(f'   Количество деревьев RF: {data[\"default_config\"][\"rf_n_estimators\"]}')
print(f'   Веса ансамбля: {data[\"default_config\"][\"ensemble_weights\"]}')
"

echo ""
echo "="*50
echo ""

# 2. Получение списка файлов
echo "2. Получение списка загруженных файлов:"
curl -X GET "http://localhost:8009/data-files" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f'   Статус: 200')
if data['files']:
    for file in data['files']:
        print(f'   Файл: {file[\"filename\"]} ({file[\"size_mb\"]} MB)')
else:
    print('   Файлы не найдены')
"

echo ""
echo "="*50
echo ""

# 3. Обучение модели с кастомными параметрами
echo "3. Обучение модели с кастомными параметрами:"
curl -X POST "http://localhost:8009/train" \
  -F "filename=test_data.csv" \
  -F 'config={"train_size": 40, "rf_n_estimators": 50, "gb_n_estimators": 50, "ensemble_weights": [1,1,1,1,1], "cv_splits": 3}' | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f'   Статус: 200')
print(f'   Сообщение: {data[\"message\"]}')
print(f'   Обученные модели: {data[\"models_trained\"]}')
print(f'   Всего признаков: {data[\"feature_count\"]}')
print(f'   Отобрано признаков: {data[\"selected_features_count\"]}')
print('   Метрики обучения:')
for target, metrics in data['training_metrics'].items():
    print(f'     {target}: CV MAE = {metrics[\"cv_mae_mean\"]:.4f}')
"

echo ""
echo "="*50
echo ""

# 4. Проверка статуса
echo "4. Проверка статуса после обучения:"
curl -X GET "http://localhost:8009/health" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f'   Статус: {data[\"status\"]}')
print(f'   Загружено моделей: {data[\"models_loaded\"]}')
print(f'   Доступные цели: {data[\"available_targets\"]}')
"

echo ""
echo "=== Демонстрация завершена ==="
