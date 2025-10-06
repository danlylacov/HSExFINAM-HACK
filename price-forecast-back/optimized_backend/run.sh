#!/bin/bash

# Скрипт для запуска оптимизированного бэкенда

echo "🚀 Запуск оптимизированного бэкенда для предсказания цен"
echo "=================================================="

# Проверяем наличие Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не найден. Установите Python3."
    exit 1
fi

# Проверяем наличие pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 не найден. Установите pip3."
    exit 1
fi

# Устанавливаем зависимости
echo "📦 Установка зависимостей..."
pip3 install -r requirements.txt

# Создаем необходимые папки
echo "📁 Создание папок..."
mkdir -p models
mkdir -p data

# Запускаем сервер
echo "🚀 Запуск сервера на порту 8010..."
echo "   API будет доступен по адресу: http://localhost:8010"
echo "   Документация: http://localhost:8010/docs"
echo ""
echo "Для остановки нажмите Ctrl+C"
echo ""

python3 main.py
