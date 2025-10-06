#!/usr/bin/env python3
"""
Скрипт для обучения оптимизированной модели
"""

import sys
import os
import json
import requests

def train_optimized_model():
    """Обучение оптимизированной модели"""
    base_url = "http://localhost:8010"
    
    print("🚀 Обучение оптимизированной модели")
    print("=" * 50)
    
    try:
        # Проверяем доступность API
        print("1. Проверка доступности API...")
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code != 200:
            print("❌ API недоступен. Запустите сервер сначала.")
            return False
        print("✅ API доступен")
        
        # Проверяем наличие данных
        print("\n2. Проверка данных...")
        response = requests.get(f"{base_url}/data-files", timeout=5)
        if response.status_code == 200:
            data_files = response.json()
            if not data_files.get('files'):
                print("❌ Нет загруженных файлов данных")
                print("   Сначала загрузите данные через /upload-data")
                return False
            
            # Используем первый доступный файл
            filename = data_files['files'][0]['filename']
            print(f"✅ Найден файл данных: {filename}")
        else:
            print("❌ Ошибка получения списка файлов")
            return False
        
        # Конфигурация обучения
        config = {
            "train_size": 25,
            "test_size": None
        }
        
        print(f"\n3. Обучение модели с конфигурацией: {config}")
        
        # Отправляем запрос на обучение
        files = {
            'filename': (None, filename),
            'config': (None, json.dumps(config))
        }
        
        response = requests.post(
            f"{base_url}/train",
            files=files,
            timeout=120  # Увеличиваем таймаут для обучения
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Обучение завершено успешно!")
            print(f"   Статус: {result['status']}")
            print(f"   Сообщение: {result['message']}")
            print(f"   Финальный score: {result['final_score']:.4f}")
            print(f"   Количество признаков: {result['feature_count']}")
            
            # Проверяем загрузку модели
            print("\n4. Проверка загрузки модели...")
            response = requests.get(f"{base_url}/health", timeout=5)
            if response.status_code == 200:
                health_data = response.json()
                if health_data.get('model_loaded'):
                    print("✅ Модель загружена и готова к использованию")
                    return True
                else:
                    print("❌ Модель не загружена")
                    return False
            else:
                print("❌ Ошибка проверки здоровья")
                return False
                
        else:
            print(f"❌ Ошибка обучения: {response.status_code}")
            print(f"   Ответ: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Не удается подключиться к API. Убедитесь, что сервер запущен.")
        return False
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

if __name__ == "__main__":
    success = train_optimized_model()
    if success:
        print("\n🎉 Обучение завершено успешно!")
        print("✅ Оптимизированная модель готова к использованию!")
    else:
        print("\n💥 Обучение не удалось!")
