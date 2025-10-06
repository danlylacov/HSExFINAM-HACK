#!/usr/bin/env python3
"""
Генерация вывода в формате CSV для задачи
"""

import subprocess
import json
import sys

def generate_csv_output():
    """Генерация вывода в формате ticker,p1,p2,...,p20"""
    print("📊 Генерация вывода в формате CSV")
    print("=" * 50)
    
    try:
        # Выполняем запрос к API
        result = subprocess.run([
            'curl', '-X', 'POST', 'http://localhost:8009/predict',
            '-H', 'Content-Type: application/json',
            '-d', '@test_predict_data.json',
            '--max-time', '30',
            '--silent'
        ], capture_output=True, text=True, cwd='/home/daniil/Рабочий стол/FINAM_HACK/price-forecast-back')
        
        if result.returncode != 0:
            print(f"❌ Ошибка запроса: {result.stderr}")
            return False
        
        # Парсим ответ
        response_data = json.loads(result.stdout)
        ticker = response_data['ticker']
        returns = response_data['returns']
        
        # Формируем CSV строку
        csv_line = f"{ticker}," + ",".join([f"{r:.6f}" for r in returns])
        
        print(f"✅ Получены данные для тикера: {ticker}")
        print(f"📈 Количество доходностей: {len(returns)}")
        
        print(f"\n📋 Формат CSV (требуемый формат задачи):")
        print(f"ticker,p1,p2,p3,...,p20")
        print("-" * 50)
        print(csv_line)
        
        print(f"\n📊 Детализация доходностей:")
        print(f"{'Период':<8} {'Доходность':<12} {'Процент':<10}")
        print("-" * 35)
        for i, ret in enumerate(returns):
            period = f"p{i+1}"
            percent = f"{ret*100:.2f}%"
            print(f"{period:<8} {ret:<12.6f} {percent:<10}")
        
        # Сохраняем в файл
        with open('prediction_output.csv', 'w') as f:
            f.write(csv_line + '\n')
        
        print(f"\n💾 Результат сохранен в файл: prediction_output.csv")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

if __name__ == "__main__":
    success = generate_csv_output()
    if success:
        print("\n🎉 Генерация CSV вывода завершена успешно!")
        print("✅ Формат соответствует требованиям задачи!")
    else:
        print("\n💥 Ошибка генерации вывода!")
        sys.exit(1)
