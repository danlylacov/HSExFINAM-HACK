#!/usr/bin/env python3
"""
Тест эндпоинта /predict с несколькими разными тикерами
"""

import subprocess
import json
import sys
from collections import defaultdict

def test_multiple_tickers():
    """Тестирование эндпоинта с несколькими тикерами"""
    print("🚀 Тестирование эндпоинта /predict с несколькими тикерами")
    print("=" * 70)
    
    # Выполняем curl запрос
    try:
        result = subprocess.run([
            'curl', '-X', 'POST', 'http://localhost:8009/predict',
            '-H', 'Content-Type: application/json',
            '-d', '@test_multiple_tickers.json',
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
        ticker = response_data.get('ticker', 'UNKNOWN')
        returns = response_data.get('returns', [])
        
        print(f"✅ Запрос выполнен успешно!")
        print(f"📊 Тикер в ответе: {ticker}")
        print(f"📈 Количество доходностей: {len(returns)}")
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
        
        # Проверяем логику выбора тикера
        print(f"\n🔍 Проверка логики выбора тикера:")
        print(f"   Тикер в ответе: {ticker}")
        print(f"   Тикер из первой записи: {input_data['params'][0]['ticker']}")
        
        if ticker == input_data['params'][0]['ticker']:
            print("   ✅ Тикер выбран из первой записи (корректно)")
        else:
            print("   ⚠️  Тикер не соответствует первой записи")
        
        # Проверяем базовую цену
        base_close_price = input_data['params'][-1]['close']
        print(f"   Базовая цена закрытия: {base_close_price}")
        print(f"   Тикер базовой цены: {input_data['params'][-1]['ticker']}")
        
        # Анализ доходностей
        print(f"\n📈 Анализ доходностей для тикера {ticker}:")
        print(f"{'Период':<8} {'Доходность':<12} {'Процент':<10}")
        print("-" * 35)
        for i, ret in enumerate(returns[:10]):  # Показываем первые 10
            period = f"p{i+1}"
            percent = f"{ret*100:.2f}%"
            print(f"{period:<8} {ret:<12.6f} {percent:<10}")
        
        if len(returns) > 10:
            print(f"... и еще {len(returns) - 10} периодов")
        
        # Статистика
        print(f"\n📊 Статистика доходностей:")
        print(f"   Минимальная доходность: {min(returns):.6f} ({min(returns)*100:.2f}%)")
        print(f"   Максимальная доходность: {max(returns):.6f} ({max(returns)*100:.2f}%)")
        print(f"   Средняя доходность: {sum(returns)/len(returns):.6f} ({sum(returns)/len(returns)*100:.2f}%)")
        
        # Проверяем разумность значений
        reasonable_returns = all(-0.5 <= r <= 0.5 for r in returns)  # Доходности в пределах ±50%
        if reasonable_returns:
            print("   ✅ Доходности в разумных пределах (±50%)")
        else:
            print("   ⚠️  Некоторые доходности выходят за разумные пределы")
        
        # Проверяем логику расчета
        print(f"\n🧮 Проверка расчетов:")
        print(f"   Базовая цена: {base_close_price}")
        print(f"   Тикер базовой цены: {input_data['params'][-1]['ticker']}")
        
        # Проверяем первые несколько расчетов
        for i in range(min(3, len(returns))):
            expected_close = base_close_price * (1 + returns[i])
            print(f"     p{i+1}: {returns[i]:.6f} -> ожидаемая цена ~{expected_close:.2f}")
        
        # Проблема с текущей реализацией
        print(f"\n⚠️  ПРОБЛЕМА С ТЕКУЩЕЙ РЕАЛИЗАЦИЕЙ:")
        print(f"   • API возвращает доходности только для одного тикера")
        print(f"   • Выбирается тикер из первой записи: {ticker}")
        print(f"   • Базовая цена берется из последней записи: {input_data['params'][-1]['ticker']}")
        print(f"   • Это может привести к некорректным расчетам!")
        
        if ticker != input_data['params'][-1]['ticker']:
            print(f"   ❌ КРИТИЧЕСКАЯ ОШИБКА: Тикер ответа ({ticker}) != Тикер базовой цены ({input_data['params'][-1]['ticker']})")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка тестирования: {e}")
        return False

if __name__ == "__main__":
    success = test_multiple_tickers()
    if success:
        print("\n🎉 Тест с несколькими тикерами завершен!")
        print("✅ API работает, но есть потенциальные проблемы с логикой!")
    else:
        print("\n💥 Тест не пройден!")
        sys.exit(1)
