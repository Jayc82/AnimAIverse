#!/bin/bash
# Quick deployment script for AnimAIverse
# Usage: ./deploy.sh [platform]
# Platforms: heroku, aws, gcp, azure, digitalocean, docker

set -e

PLATFORM=${1:-heroku}
APP_NAME=${2:-animaiverse-app}

echo "🚀 Deploying AnimAIverse to $PLATFORM..."

case $PLATFORM in
  heroku)
    echo "📦 Deploying to Heroku..."
    
    # Check if Heroku CLI is installed
    if ! command -v heroku &> /dev/null; then
        echo "❌ Heroku CLI not found. Install from: https://devcenter.heroku.com/articles/heroku-cli"
        exit 1
    fi
    
    # Check if logged in
    heroku whoami > /dev/null 2>&1 || heroku login
    
    # Create app if it doesn't exist
    if heroku apps:info --app $APP_NAME &> /dev/null; then
        echo "✓ App $APP_NAME already exists"
    else
        echo "Creating new Heroku app: $APP_NAME"
        heroku create $APP_NAME
    fi
    
    # Add buildpack
    heroku buildpacks:set heroku/python --app $APP_NAME
    
    # Set environment variables (if not already set)
    if [ ! -z "$OPENAI_API_KEY" ]; then
        heroku config:set OPENAI_API_KEY=$OPENAI_API_KEY --app $APP_NAME
    fi
    if [ ! -z "$ANTHROPIC_API_KEY" ]; then
        heroku config:set ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY --app $APP_NAME
    fi
    
    # Deploy
    git push heroku main || git push heroku HEAD:main
    
    # Open app
    heroku open --app $APP_NAME
    
    echo "✅ Deployed successfully to Heroku!"
    ;;
    
  aws)
    echo "📦 Deploying to AWS Elastic Beanstalk..."
    
    if ! command -v eb &> /dev/null; then
        echo "❌ AWS EB CLI not found. Install with: pip install awsebcli"
        exit 1
    fi
    
    # Initialize if not already done
    if [ ! -d ".elasticbeanstalk" ]; then
        eb init -p python-3.11 $APP_NAME --region us-east-1
    fi
    
    # Create environment if needed
    eb create $APP_NAME-production || eb deploy
    
    # Set environment variables
    if [ ! -z "$OPENAI_API_KEY" ]; then
        eb setenv OPENAI_API_KEY=$OPENAI_API_KEY
    fi
    if [ ! -z "$ANTHROPIC_API_KEY" ]; then
        eb setenv ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY
    fi
    
    eb open
    
    echo "✅ Deployed successfully to AWS!"
    ;;
    
  gcp)
    echo "📦 Deploying to Google Cloud Platform..."
    
    if ! command -v gcloud &> /dev/null; then
        echo "❌ Google Cloud SDK not found. Install from: https://cloud.google.com/sdk/docs/install"
        exit 1
    fi
    
    # Deploy
    gcloud app deploy app.yaml --quiet
    
    # Open app
    gcloud app browse
    
    echo "✅ Deployed successfully to GCP!"
    ;;
    
  azure)
    echo "📦 Deploying to Microsoft Azure..."
    
    if ! command -v az &> /dev/null; then
        echo "❌ Azure CLI not found. Install from: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
        exit 1
    fi
    
    # Login if needed
    az account show > /dev/null 2>&1 || az login
    
    # Create resource group
    az group create --name ${APP_NAME}RG --location eastus
    
    # Create app service plan
    az appservice plan create --name ${APP_NAME}Plan --resource-group ${APP_NAME}RG --sku B1 --is-linux
    
    # Create web app
    az webapp create --resource-group ${APP_NAME}RG --plan ${APP_NAME}Plan --name $APP_NAME --runtime "PYTHON:3.11"
    
    # Set environment variables
    if [ ! -z "$OPENAI_API_KEY" ]; then
        az webapp config appsettings set --resource-group ${APP_NAME}RG --name $APP_NAME \
            --settings OPENAI_API_KEY=$OPENAI_API_KEY
    fi
    if [ ! -z "$ANTHROPIC_API_KEY" ]; then
        az webapp config appsettings set --resource-group ${APP_NAME}RG --name $APP_NAME \
            --settings ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY
    fi
    
    # Deploy
    az webapp up --name $APP_NAME --resource-group ${APP_NAME}RG
    
    echo "✅ Deployed successfully to Azure!"
    ;;
    
  digitalocean)
    echo "📦 Deploying to DigitalOcean..."
    
    if ! command -v doctl &> /dev/null; then
        echo "❌ doctl not found. Install from: https://docs.digitalocean.com/reference/doctl/how-to/install/"
        exit 1
    fi
    
    # Check auth
    doctl auth list > /dev/null 2>&1 || doctl auth init
    
    # Create app
    doctl apps create --spec .do/app.yaml
    
    echo "✅ Deployment initiated on DigitalOcean!"
    echo "Check status at: https://cloud.digitalocean.com/apps"
    ;;
    
  docker)
    echo "📦 Deploying with Docker..."
    
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker not found. Install from: https://docs.docker.com/get-docker/"
        exit 1
    fi
    
    # Build image
    echo "Building Docker image..."
    docker build -t animaiverse:latest .
    
    # Stop existing container
    docker stop animaiverse 2>/dev/null || true
    docker rm animaiverse 2>/dev/null || true
    
    # Run container
    echo "Starting container..."
    docker run -d \
        -p 5000:5000 \
        -e OPENAI_API_KEY=${OPENAI_API_KEY} \
        -e ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY} \
        -v $(pwd)/memory:/app/memory \
        --name animaiverse \
        animaiverse:latest
    
    echo "✅ Docker container started successfully!"
    echo "Access at: http://localhost:5000"
    ;;
    
  *)
    echo "❌ Unknown platform: $PLATFORM"
    echo "Supported platforms: heroku, aws, gcp, azure, digitalocean, docker"
    exit 1
    ;;
esac

echo ""
echo "🎉 Deployment complete!"
echo "Your AnimAIverse is now live and ready to create revolutionary animations!"
