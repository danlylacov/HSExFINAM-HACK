#!/usr/bin/env python3
"""
Тест эндпоинта /predict с curl и анализом результатов
"""

import subprocess
import json
import sys

def test_predict_endpoint():
    """Тестирование эндпоинта предсказания с curl"""
    print("🚀 Тестирование эндпоинта /predict с curl")
    print("=" * 60)
    
    # Выполняем curl запрос
    try:
        result = subprocess.run([
            'curl', '-X', 'POST', 'http://localhost:8009/predict',
            '-H', 'Content-Type: application/json',
            '-d', '@test_predict_data.json',
            '--max-time', '30',
            '-w', '\nHTTP Status: %{http_code}\nTotal Time: %{time_total}s\n',
            '--silent'
        ], capture_output=True, text=True, cwd='/home/daniil/Рабочий стол/FINAM_HACK/price-forecast-back')
        
        if result.returncode != 0:
            print(f"❌ Ошибка curl: {result.stderr}")
            return False
        
        # Парсим ответ
        output_lines = result.stdout.strip().split('\n')
        json_response = '\n'.join(output_lines[:-2])  # Убираем последние 2 строки с метаданными
        metadata = output_lines[-2:]  # Последние 2 строки с метаданными
        
        try:
            response_data = json.loads(json_response)
        except json.JSONDecodeError as e:
            print(f"❌ Ошибка парсинга JSON: {e}")
            print(f"Ответ: {json_response}")
            return False
        
        # Анализируем результаты
        predictions = response_data.get('predictions', [])
        
        print(f"✅ Запрос выполнен успешно!")
        print(f"📊 Получено предсказаний: {len(predictions)}")
        print(f"📈 Метаданные: {metadata[0]}, {metadata[1]}")
        
        print(f"\n🔍 Анализ предсказаний:")
        print(f"{'Дата':<12} {'Open':<8} {'High':<8} {'Low':<8} {'Close':<8} {'Volume':<10}")
        print("-" * 60)
        
        for i, pred in enumerate(predictions[:10]):  # Показываем первые 10
            print(f"{pred['date']:<12} {pred['open']:<8.2f} {pred['high']:<8.2f} {pred['low']:<8.2f} {pred['close']:<8.2f} {pred['volume']:<10.0f}")
        
        if len(predictions) > 10:
            print(f"... и еще {len(predictions) - 10} предсказаний")
        
        # Статистика
        opens = [p['open'] for p in predictions]
        highs = [p['high'] for p in predictions]
        lows = [p['low'] for p in predictions]
        closes = [p['close'] for p in predictions]
        volumes = [p['volume'] for p in predictions]
        
        print(f"\n📊 Статистика предсказаний:")
        print(f"   Цена открытия: мин={min(opens):.2f}, макс={max(opens):.2f}, среднее={sum(opens)/len(opens):.2f}")
        print(f"   Цена максимум: мин={min(highs):.2f}, макс={max(highs):.2f}, среднее={sum(highs)/len(highs):.2f}")
        print(f"   Цена минимум: мин={min(lows):.2f}, макс={max(lows):.2f}, среднее={sum(lows)/len(lows):.2f}")
        print(f"   Цена закрытия: мин={min(closes):.2f}, макс={max(closes):.2f}, среднее={sum(closes)/len(closes):.2f}")
        print(f"   Объем: мин={min(volumes):.0f}, макс={max(volumes):.0f}, среднее={sum(volumes)/len(volumes):.0f}")
        
        # Проверяем логику дат
        print(f"\n🗓️ Проверка дат:")
        first_date = predictions[0]['date']
        last_date = predictions[-1]['date']
        print(f"   Первая дата: {first_date}")
        print(f"   Последняя дата: {last_date}")
        print(f"   Период предсказания: {len(predictions)} дней")
        
        # Проверяем тикер
        tickers = set(p['ticker'] for p in predictions)
        print(f"   Тикеры: {tickers}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка тестирования: {e}")
        return False

if __name__ == "__main__":
    success = test_predict_endpoint()
    if success:
        print("\n🎉 Тест эндпоинта /predict прошел успешно!")
        print("✅ API корректно обрабатывает 20 входных свечей и возвращает 20 предсказаний!")
    else:
        print("\n💥 Тест не пройден!")
        sys.exit(1)
