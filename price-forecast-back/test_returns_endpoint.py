#!/usr/bin/env python3
"""
Тест обновленного эндпоинта /predict с доходностями
"""

import subprocess
import json
import sys

def test_returns_endpoint():
    """Тестирование эндпоинта предсказания доходностей"""
    print("🚀 Тестирование обновленного эндпоинта /predict (доходности)")
    print("=" * 70)
    
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
        ticker = response_data.get('ticker', 'UNKNOWN')
        returns = response_data.get('returns', [])
        
        print(f"✅ Запрос выполнен успешно!")
        print(f"📊 Тикер: {ticker}")
        print(f"📈 Количество доходностей: {len(returns)}")
        print(f"📈 Метаданные: {metadata[0]}, {metadata[1]}")
        
        # Проверяем формат ответа
        print(f"\n🔍 Проверка формата ответа:")
        if 'ticker' in response_data and 'returns' in response_data:
            print("   ✅ Формат ответа корректен: {ticker, returns}")
        else:
            print("   ❌ Неверный формат ответа")
            return False
        
        if len(returns) == 20:
            print("   ✅ Количество доходностей: 20 (корректно)")
        else:
            print(f"   ❌ Неверное количество доходностей: {len(returns)} (ожидается 20)")
            return False
        
        # Анализ доходностей
        print(f"\n📊 Анализ доходностей:")
        print(f"{'Период':<8} {'Доходность':<12} {'Описание':<20}")
        print("-" * 45)
        
        for i, ret in enumerate(returns[:10]):  # Показываем первые 10
            period = f"p{i+1}"
            description = "Рост" if ret > 0 else "Падение" if ret < 0 else "Без изменений"
            print(f"{period:<8} {ret:<12.6f} {description:<20}")
        
        if len(returns) > 10:
            print(f"... и еще {len(returns) - 10} периодов")
        
        # Статистика
        print(f"\n📈 Статистика доходностей:")
        print(f"   Минимальная доходность: {min(returns):.6f} ({min(returns)*100:.2f}%)")
        print(f"   Максимальная доходность: {max(returns):.6f} ({max(returns)*100:.2f}%)")
        print(f"   Средняя доходность: {sum(returns)/len(returns):.6f} ({sum(returns)/len(returns)*100:.2f}%)")
        
        # Проверяем логику расчета
        print(f"\n🧮 Проверка логики расчета:")
        
        # Загружаем входные данные для проверки базовой цены
        with open('test_predict_data.json', 'r') as f:
            input_data = json.load(f)
        
        base_close_price = input_data['params'][-1]['close']  # Последняя цена в истории
        print(f"   Базовая цена закрытия: {base_close_price}")
        
        # Проверяем первые несколько расчетов
        print(f"   Проверка расчетов:")
        for i in range(min(3, len(returns))):
            # Примерный расчет ожидаемой цены (используем данные из предыдущего теста)
            expected_close = base_close_price * (1 + returns[i])
            print(f"     p{i+1}: {returns[i]:.6f} -> ожидаемая цена ~{expected_close:.2f}")
        
        # Проверяем разумность значений
        reasonable_returns = all(-0.5 <= r <= 0.5 for r in returns)  # Доходности в пределах ±50%
        if reasonable_returns:
            print("   ✅ Доходности в разумных пределах (±50%)")
        else:
            print("   ⚠️  Некоторые доходности выходят за разумные пределы")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка тестирования: {e}")
        return False

if __name__ == "__main__":
    success = test_returns_endpoint()
    if success:
        print("\n🎉 Тест обновленного эндпоинта /predict прошел успешно!")
        print("✅ API теперь возвращает доходности в формате {ticker, returns}!")
        print("✅ Формат соответствует требованиям задачи!")
    else:
        print("\n💥 Тест не пройден!")
        sys.exit(1)
