# Docker Deployment для Price Prediction API

## 🐳 Быстрый старт

### 1. Сборка и запуск

```bash
# Сделать скрипт исполняемым
chmod +x docker-manage.sh

# Запустить сервис
./docker-manage.sh start
```

### 2. Проверка работы

```bash
# Проверить статус
./docker-manage.sh status

# Проверить здоровье API
./docker-manage.sh health

# Посмотреть логи
./docker-manage.sh logs
```

## 📋 Доступные команды

| Команда | Описание |
|---------|----------|
| `./docker-manage.sh start` | Запустить сервис |
| `./docker-manage.sh stop` | Остановить сервис |
| `./docker-manage.sh restart` | Перезапустить сервис |
| `./docker-manage.sh build` | Собрать образ |
| `./docker-manage.sh logs` | Показать логи |
| `./docker-manage.sh status` | Показать статус |
| `./docker-manage.sh health` | Проверить здоровье API |
| `./docker-manage.sh clean` | Очистить Docker ресурсы |

## 🔧 Ручное управление

### Docker Compose команды

```bash
# Запуск
docker-compose up -d

# Остановка
docker-compose down

# Пересборка
docker-compose build --no-cache

# Логи
docker-compose logs -f price-prediction-api

# Статус
docker-compose ps
```

### Docker команды

```bash
# Сборка образа
docker build -t price-prediction-api .

# Запуск контейнера
docker run -d \
  --name price-prediction-api \
  -p 8009:8009 \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/data:/app/data \
  price-prediction-api

# Остановка контейнера
docker stop price-prediction-api
docker rm price-prediction-api
```

## 📊 Доступ к API

После запуска API будет доступен по адресам:

- **API**: http://localhost:8009
- **Документация**: http://localhost:8009/docs
- **Health Check**: http://localhost:8009/health

## 📁 Структура томов

```
./models/  -> /app/models    # Обученные модели
./data/    -> /app/data      # Данные для обучения
```

## ⚙️ Конфигурация

### Переменные окружения

- `PYTHONUNBUFFERED=1` - Небуферизованный вывод Python

### Ресурсы

- **Память**: до 2GB
- **CPU**: до 1 ядра
- **Минимум**: 512MB RAM, 0.5 CPU

## 🚨 Устранение неполадок

### Проблема: Контейнер не запускается

```bash
# Проверить логи
./docker-manage.sh logs

# Проверить статус
./docker-manage.sh status

# Пересобрать образ
./docker-manage.sh build
```

### Проблема: API недоступен

```bash
# Проверить здоровье
./docker-manage.sh health

# Проверить порты
docker-compose ps

# Проверить логи
./docker-manage.sh logs
```

### Проблема: Модели не загружаются

```bash
# Проверить монтирование томов
docker-compose exec price-prediction-api ls -la /app/models

# Проверить права доступа
docker-compose exec price-prediction-api ls -la /app/
```

## 🔄 Обновление

```bash
# Остановить сервис
./docker-manage.sh stop

# Обновить код
git pull

# Пересобрать и запустить
./docker-manage.sh build
./docker-manage.sh start
```

## 🧹 Очистка

```bash
# Остановить и удалить контейнеры
./docker-manage.sh clean

# Удалить неиспользуемые образы
docker image prune -f

# Полная очистка Docker
docker system prune -af
```

## 📈 Мониторинг

### Проверка ресурсов

```bash
# Использование ресурсов контейнера
docker stats price-prediction-api

# Информация о контейнере
docker inspect price-prediction-api
```

### Логи

```bash
# Последние логи
docker-compose logs --tail=100 price-prediction-api

# Логи в реальном времени
docker-compose logs -f price-prediction-api
```

## 🔒 Безопасность

- Контейнер запускается от непривилегированного пользователя `app`
- Используется минимальный образ `python:3.10-slim`
- Ограничены ресурсы контейнера
- Настроен health check

## 📝 Примечания

- Для продакшена рекомендуется использовать внешний reverse proxy (nginx)
- Настройте мониторинг и логирование
- Используйте внешние базы данных для персистентности
- Настройте автоматические бэкапы моделей
