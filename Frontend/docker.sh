#!/bin/bash

# Docker management script for FINAM Frontend

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to show help
show_help() {
    echo "Docker Management Script for FINAM Frontend"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  build     Build production image"
    echo "  dev       Start development environment"
    echo "  prod      Start production environment"
    echo "  stop      Stop all containers"
    echo "  clean     Clean up Docker resources"
    echo "  logs      Show container logs"
    echo "  health    Check container health"
    echo "  help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 build    # Build production image"
    echo "  $0 dev      # Start development server"
    echo "  $0 prod     # Start production server"
    echo "  $0 stop     # Stop all containers"
}

# Function to build production image
build_production() {
    print_status "Building production image..."
    docker-compose build frontend
    print_success "Production image built successfully!"
}

# Function to start development environment
start_development() {
    print_status "Starting development environment..."
    docker-compose --profile dev up frontend-dev --build
}

# Function to start production environment
start_production() {
    print_status "Starting production environment..."
    docker-compose up frontend --build -d
    print_success "Production environment started!"
    print_status "Application available at: http://localhost:3000"
}

# Function to stop all containers
stop_containers() {
    print_status "Stopping all containers..."
    docker-compose down
    print_success "All containers stopped!"
}

# Function to clean up Docker resources
clean_docker() {
    print_warning "This will remove all unused Docker resources. Continue? (y/N)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        print_status "Cleaning up Docker resources..."
        docker system prune -a -f
        print_success "Docker cleanup completed!"
    else
        print_status "Cleanup cancelled."
    fi
}

# Function to show logs
show_logs() {
    print_status "Showing container logs..."
    docker-compose logs -f
}

# Function to check health
check_health() {
    print_status "Checking container health..."
    
    # Check if containers are running
    if docker-compose ps | grep -q "Up"; then
        print_success "Containers are running!"
        
        # Check health endpoint
        if curl -f http://localhost:3000/health > /dev/null 2>&1; then
            print_success "Health check passed!"
        else
            print_warning "Health check failed or container not ready yet."
        fi
    else
        print_error "No containers are running!"
    fi
}

# Main script logic
case "${1:-help}" in
    build)
        build_production
        ;;
    dev)
        start_development
        ;;
    prod)
        start_production
        ;;
    stop)
        stop_containers
        ;;
    clean)
        clean_docker
        ;;
    logs)
        show_logs
        ;;
    health)
        check_health
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        echo ""
        show_help
        exit 1
        ;;
esac
