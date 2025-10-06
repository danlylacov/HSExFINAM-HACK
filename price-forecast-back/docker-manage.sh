#!/bin/bash

# Скрипт управления Docker Compose для Price Prediction API

case "$1" in
    "start")
        echo "🚀 Запуск Price Prediction API..."
        docker-compose up -d
        echo "✅ Сервис запущен"
        echo "📊 API доступен по адресу: http://localhost:8009"
        echo "📚 Документация: http://localhost:8009/docs"
        ;;
    "stop")
        echo "🛑 Остановка Price Prediction API..."
        docker-compose down
        echo "✅ Сервис остановлен"
        ;;
    "restart")
        echo "🔄 Перезапуск Price Prediction API..."
        docker-compose down
        docker-compose up -d
        echo "✅ Сервис перезапущен"
        ;;
    "build")
        echo "🔨 Сборка образа Price Prediction API..."
        docker-compose build --no-cache
        echo "✅ Образ собран"
        ;;
    "logs")
        echo "📋 Логи Price Prediction API..."
        docker-compose logs -f price-prediction-api
        ;;
    "status")
        echo "📊 Статус сервисов:"
        docker-compose ps
        ;;
    "health")
        echo "🏥 Проверка здоровья API..."
        curl -f http://localhost:8009/health || echo "❌ API недоступен"
        ;;
    "clean")
        echo "🧹 Очистка Docker ресурсов..."
        docker-compose down -v
        docker system prune -f
        echo "✅ Очистка завершена"
        ;;
    *)
        echo "📖 Использование: $0 {start|stop|restart|build|logs|status|health|clean}"
        echo ""
        echo "Команды:"
        echo "  start   - Запустить сервис"
        echo "  stop    - Остановить сервис"
        echo "  restart - Перезапустить сервис"
        echo "  build   - Собрать образ"
        echo "  logs    - Показать логи"
        echo "  status  - Показать статус"
        echo "  health  - Проверить здоровье API"
        echo "  clean   - Очистить Docker ресурсы"
        exit 1
        ;;
esac
