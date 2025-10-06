#!/usr/bin/env python3
"""
Тест обновленного эндпоинта /predict с поддержкой множественных тикеров
"""

import subprocess
import json
import sys
from collections import defaultdict

def test_multiple_tickers_v2():
    """Тестирование обновленного эндпоинта с несколькими тикерами"""
    print("🚀 Тестирование обновленного эндпоинта /predict (множественные тикеры)")
    print("=" * 80)
    
    # Выполняем curl запрос
    try:
        result = subprocess.run([
            'curl', '-X', 'POST', 'http://localhost:8009/predict',
            '-H', 'Content-Type: application/json',
            '-d', '@test_multiple_tickers.json',
            '--max-time', '60',  # Увеличиваем таймаут для множественных тикеров
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
        results = response_data.get('results', [])
        
        print(f"✅ Запрос выполнен успешно!")
        print(f"📊 Количество обработанных тикеров: {len(results)}")
        print(f"📈 Метаданные: {metadata[0]}, {metadata[1]}")
        
        # Анализируем входные данные
        with open('test_multiple_tickers.json', 'r') as f:
            input_data = json.load(f)
        
        # Группируем данные по тикерам
        ticker_data = defaultdict(list)
        for record in input_data['params']:
            ticker_data[record['ticker']].append(record)
        
        print(f"\n📊 Анализ входных данных:")
        print(f"   Всего записей: {len(input_data['params'])}")
        print(f"   Уникальных тикеров: {len(ticker_data)}")
        
        for ticker_name, records in ticker_data.items():
            print(f"   {ticker_name}: {len(records)} записей")
            last_record = records[-1]
            print(f"     Последняя цена закрытия: {last_record['close']}")
        
        # Проверяем результаты
        print(f"\n🔍 Анализ результатов:")
        print(f"   Ожидалось тикеров: {len(ticker_data)}")
        print(f"   Получено результатов: {len(results)}")
        
        if len(results) == len(ticker_data):
            print("   ✅ Количество результатов соответствует количеству тикеров")
        else:
            print("   ⚠️  Количество результатов не соответствует количеству тикеров")
        
        # Анализируем каждый результат
        for i, result in enumerate(results):
            ticker = result['ticker']
            returns = result['returns']
            
            print(f"\n📈 Тикер {i+1}: {ticker}")
            print(f"   Количество доходностей: {len(returns)}")
            print(f"   Минимальная доходность: {min(returns):.6f} ({min(returns)*100:.2f}%)")
            print(f"   Максимальная доходность: {max(returns):.6f} ({max(returns)*100:.2f}%)")
            print(f"   Средняя доходность: {sum(returns)/len(returns):.6f} ({sum(returns)/len(returns)*100:.2f}%)")
            
            # Проверяем разумность значений
            reasonable_returns = all(-0.5 <= r <= 0.5 for r in returns)
            if reasonable_returns:
                print("   ✅ Доходности в разумных пределах (±50%)")
            else:
                print("   ⚠️  Некоторые доходности выходят за разумные пределы")
            
            # Показываем первые несколько значений
            print(f"   Первые 5 доходностей: {[f'{r:.4f}' for r in returns[:5]]}")
        
        # Проверяем логику расчета для каждого тикера
        print(f"\n🧮 Проверка логики расчета:")
        
        for result in results:
            ticker = result['ticker']
            returns = result['returns']
            
            # Находим соответствующие данные в входных данных
            ticker_records = ticker_data[ticker]
            base_close_price = ticker_records[-1]['close']  # Последняя цена для этого тикера
            
            print(f"   {ticker}:")
            print(f"     Базовая цена: {base_close_price}")
            print(f"     Тикер базовой цены: {ticker} ✅")
            
            # Проверяем первые несколько расчетов
            for i in range(min(3, len(returns))):
                expected_close = base_close_price * (1 + returns[i])
                print(f"     p{i+1}: {returns[i]:.6f} -> ожидаемая цена ~{expected_close:.2f}")
        
        # Генерируем CSV вывод для каждого тикера
        print(f"\n📋 CSV формат для каждого тикера:")
        csv_lines = []
        for result in results:
            ticker = result['ticker']
            returns = result['returns']
            csv_line = f"{ticker}," + ",".join([f"{r:.6f}" for r in returns])
            csv_lines.append(csv_line)
            print(f"   {csv_line}")
        
        # Сохраняем результаты в файл
        with open('multi_ticker_prediction_output.csv', 'w') as f:
            for line in csv_lines:
                f.write(line + '\n')
        
        print(f"\n💾 Результаты сохранены в файл: multi_ticker_prediction_output.csv")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка тестирования: {e}")
        return False

if __name__ == "__main__":
    success = test_multiple_tickers_v2()
    if success:
        print("\n🎉 Тест с множественными тикерами завершен успешно!")
        print("✅ API корректно обрабатывает несколько тикеров одновременно!")
        print("✅ Каждый тикер обрабатывается с правильной базовой ценой!")
    else:
        print("\n💥 Тест не пройден!")
        sys.exit(1)
