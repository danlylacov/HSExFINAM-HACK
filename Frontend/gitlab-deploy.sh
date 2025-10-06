#!/bin/bash

# GitLab Deployment Script for FINAM Frontend

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
GITLAB_URL="gitlab.com"
PROJECT_PATH="your-group/finam-frontend"  # Change this to your project path
REGISTRY_URL="registry.gitlab.com"

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
    echo "GitLab Deployment Script for FINAM Frontend"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  init       Initialize Git repository and remote"
    echo "  deploy     Deploy to GitLab (build + push)"
    echo "  staging    Deploy to staging environment"
    echo "  production Deploy to production environment"
    echo "  status     Check deployment status"
    echo "  logs       Show deployment logs"
    echo "  help       Show this help message"
    echo ""
    echo "Configuration:"
    echo "  Edit PROJECT_PATH variable in this script"
    echo "  Current: $PROJECT_PATH"
    echo ""
    echo "Examples:"
    echo "  $0 init      # Initialize repository"
    echo "  $0 deploy    # Deploy to GitLab"
    echo "  $0 staging   # Deploy to staging"
}

# Function to check if git is initialized
check_git() {
    if [ ! -d ".git" ]; then
        print_error "Git repository not initialized!"
        print_status "Run: $0 init"
        exit 1
    fi
}

# Function to initialize Git repository
init_repo() {
    print_status "Initializing Git repository..."
    
    if [ ! -d ".git" ]; then
        git init
        print_success "Git repository initialized!"
    else
        print_warning "Git repository already exists!"
    fi
    
    # Check if remote exists
    if ! git remote get-url origin > /dev/null 2>&1; then
        print_status "Adding GitLab remote..."
        git remote add origin "git@$GITLAB_URL:$PROJECT_PATH.git"
        print_success "Remote added: git@$GITLAB_URL:$PROJECT_PATH.git"
    else
        print_warning "Remote already exists!"
    fi
    
    # Create .gitignore if it doesn't exist
    if [ ! -f ".gitignore" ]; then
        print_status "Creating .gitignore..."
        cat > .gitignore << 'EOF'
# Dependencies
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Build outputs
dist/
build/

# Environment files
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# IDE files
.vscode/
.idea/
*.swp
*.swo

# OS files
.DS_Store
Thumbs.db

# Logs
logs/
*.log

# Coverage directory
coverage/

# Temporary folders
tmp/
temp/
EOF
        print_success ".gitignore created!"
    fi
    
    print_success "Repository initialization complete!"
    print_status "Next steps:"
    print_status "1. Edit PROJECT_PATH in this script if needed"
    print_status "2. Run: $0 deploy"
}

# Function to deploy to GitLab
deploy_to_gitlab() {
    check_git
    
    print_status "Deploying to GitLab..."
    
    # Check if there are changes
    if git diff --quiet && git diff --cached --quiet; then
        print_warning "No changes to commit!"
        print_status "Make some changes first, then run: $0 deploy"
        exit 0
    fi
    
    # Add all changes
    print_status "Adding changes..."
    git add .
    
    # Get commit message
    if [ -z "$1" ]; then
        COMMIT_MSG="Deploy: $(date '+%Y-%m-%d %H:%M:%S')"
    else
        COMMIT_MSG="$1"
    fi
    
    # Commit changes
    print_status "Committing changes..."
    git commit -m "$COMMIT_MSG"
    
    # Push to GitLab
    print_status "Pushing to GitLab..."
    git push origin main
    
    print_success "Deployment to GitLab complete!"
    print_status "Check CI/CD pipeline at: https://$GITLAB_URL/$PROJECT_PATH/-/pipelines"
}

# Function to deploy to staging
deploy_staging() {
    print_status "Deploying to staging environment..."
    
    # This would typically involve SSH to staging server
    print_warning "Staging deployment not configured!"
    print_status "Configure staging server details in this script"
    print_status "Or deploy manually:"
    print_status "docker pull $REGISTRY_URL/$PROJECT_PATH:latest"
    print_status "docker run -d --name finam-staging -p 3001:80 $REGISTRY_URL/$PROJECT_PATH:latest"
}

# Function to deploy to production
deploy_production() {
    print_status "Deploying to production environment..."
    
    # This would typically involve SSH to production server
    print_warning "Production deployment not configured!"
    print_status "Configure production server details in this script"
    print_status "Or deploy manually:"
    print_status "docker pull $REGISTRY_URL/$PROJECT_PATH:latest"
    print_status "docker run -d --name finam-production -p 80:80 $REGISTRY_URL/$PROJECT_PATH:latest"
}

# Function to check deployment status
check_status() {
    print_status "Checking deployment status..."
    
    # Check GitLab pipeline status
    print_status "GitLab Pipeline: https://$GITLAB_URL/$PROJECT_PATH/-/pipelines"
    
    # Check if we can pull the latest image
    print_status "Testing Docker image pull..."
    if docker pull "$REGISTRY_URL/$PROJECT_PATH:latest" > /dev/null 2>&1; then
        print_success "Docker image is available!"
    else
        print_error "Docker image not found or not accessible!"
    fi
}

# Function to show logs
show_logs() {
    print_status "Showing deployment logs..."
    
    # Show recent Git commits
    print_status "Recent commits:"
    git log --oneline -5
    
    # Show GitLab pipeline status
    print_status "Check pipeline logs at: https://$GITLAB_URL/$PROJECT_PATH/-/pipelines"
}

# Main script logic
case "${1:-help}" in
    init)
        init_repo
        ;;
    deploy)
        deploy_to_gitlab "$2"
        ;;
    staging)
        deploy_staging
        ;;
    production)
        deploy_production
        ;;
    status)
        check_status
        ;;
    logs)
        show_logs
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
