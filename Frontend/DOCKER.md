# Docker Setup for Frontend

Этот проект настроен для работы с Docker. Доступны два режима: production и development.

## 🚀 Быстрый старт

### Production (рекомендуется)

```bash
# Сборка и запуск production версии
docker-compose up --build

# Приложение будет доступно по адресу: http://localhost:3000
```

### Development

```bash
# Запуск development версии с hot reload
docker-compose --profile dev up frontend-dev --build

# Приложение будет доступно по адресу: http://localhost:5173
```

## 📋 Доступные команды

### Production
```bash
# Сборка образа
docker build -t finam-frontend .

# Запуск контейнера
docker run -p 3000:80 finam-frontend

# Остановка
docker-compose down
```

### Development
```bash
# Сборка development образа
docker build -f Dockerfile.dev -t finam-frontend-dev .

# Запуск development контейнера
docker run -p 5173:5173 -v $(pwd):/app -v /app/node_modules finam-frontend-dev
```

## 🔧 Конфигурация

### Порты
- **Production**: 3000 → 80 (nginx)
- **Development**: 5173 → 5173 (vite dev server)

### Переменные окружения
- `NODE_ENV`: production/development

### Health Check
- Endpoint: `/health`
- Проверка каждые 30 секунд

## 📁 Структура Docker файлов

```
├── Dockerfile          # Production build
├── Dockerfile.dev      # Development build
├── docker-compose.yml  # Orchestration
├── nginx.conf         # Nginx configuration
└── .dockerignore      # Ignore files
```

## 🛠 Troubleshooting

### Проблемы с портами
```bash
# Проверить занятые порты
netstat -tulpn | grep :3000
netstat -tulpn | grep :5173

# Остановить все контейнеры
docker-compose down
```

### Проблемы с кэшем
```bash
# Пересобрать без кэша
docker-compose build --no-cache

# Очистить все образы
docker system prune -a
```

### Логи
```bash
# Просмотр логов
docker-compose logs frontend
docker-compose logs frontend-dev

# Следить за логами в реальном времени
docker-compose logs -f frontend
```

## 🌐 Nginx Features

- **SPA Support**: Client-side routing
- **Gzip Compression**: Автоматическое сжатие
- **Static Assets Caching**: Кэширование статических файлов
- **Security Headers**: Базовые заголовки безопасности
- **Health Check**: Endpoint для мониторинга

## 📦 Размер образов

- **Production**: ~25MB (nginx + built assets)
- **Development**: ~200MB (node + dependencies)

## 🔄 CI/CD Integration

```yaml
# Пример GitHub Actions
- name: Build and push Docker image
  run: |
    docker build -t ${{ secrets.DOCKER_REGISTRY }}/finam-frontend:${{ github.sha }} .
    docker push ${{ secrets.DOCKER_REGISTRY }}/finam-frontend:${{ github.sha }}
```
