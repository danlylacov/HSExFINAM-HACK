# Makefile for FINAM Frontend Docker Management

.PHONY: help build dev prod stop clean logs health install

# Default target
help:
	@echo "FINAM Frontend Docker Management"
	@echo ""
	@echo "Available targets:"
	@echo "  build     - Build production Docker image"
	@echo "  dev       - Start development environment with hot reload"
	@echo "  prod      - Start production environment"
	@echo "  stop      - Stop all Docker containers"
	@echo "  clean     - Clean up Docker resources"
	@echo "  logs      - Show container logs"
	@echo "  health    - Check container health"
	@echo "  install   - Install dependencies locally"
	@echo ""
	@echo "Examples:"
	@echo "  make build    # Build production image"
	@echo "  make dev      # Start development server"
	@echo "  make prod     # Start production server"

# Build production image
build:
	@echo "Building production image..."
	docker-compose build frontend
	@echo "✅ Production image built successfully!"

# Start development environment
dev:
	@echo "Starting development environment..."
	docker-compose --profile dev up frontend-dev --build

# Start production environment
prod:
	@echo "Starting production environment..."
	docker-compose up frontend --build -d
	@echo "✅ Production environment started!"
	@echo "🌐 Application available at: http://localhost:3000"

# Stop all containers
stop:
	@echo "Stopping all containers..."
	docker-compose down
	@echo "✅ All containers stopped!"

# Clean up Docker resources
clean:
	@echo "⚠️  This will remove all unused Docker resources."
	@read -p "Continue? (y/N): " confirm && [ "$$confirm" = "y" ] || exit 1
	@echo "Cleaning up Docker resources..."
	docker system prune -a -f
	@echo "✅ Docker cleanup completed!"

# Show container logs
logs:
	@echo "Showing container logs..."
	docker-compose logs -f

# Check container health
health:
	@echo "Checking container health..."
	@if docker-compose ps | grep -q "Up"; then \
		echo "✅ Containers are running!"; \
		if curl -f http://localhost:3000/health > /dev/null 2>&1; then \
			echo "✅ Health check passed!"; \
		else \
			echo "⚠️  Health check failed or container not ready yet."; \
		fi; \
	else \
		echo "❌ No containers are running!"; \
	fi

# Install dependencies locally
install:
	@echo "Installing dependencies..."
	npm install
	@echo "✅ Dependencies installed!"

# Quick start for development
quick-dev: install dev

# Quick start for production
quick-prod: build prod
