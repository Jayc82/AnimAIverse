# AnimAIverse Deployment Guide

Complete guide to deploying AnimAIverse to various platforms - from local development to cloud production.

## Table of Contents

1. [Quick Local Deployment](#quick-local-deployment)
2. [Production Deployment Options](#production-deployment-options)
3. [Cloud Platforms](#cloud-platforms)
4. [Docker Deployment](#docker-deployment)
5. [Environment Configuration](#environment-configuration)
6. [Monitoring & Scaling](#monitoring--scaling)

---

## Quick Local Deployment

### Prerequisites

- Python 3.8 or higher
- pip package manager
- 2GB RAM minimum (4GB+ recommended)
- API keys for AI services (OpenAI, Anthropic)

### Step 1: Install Dependencies

```bash
# Clone the repository (if not already done)
git clone https://github.com/Jayc82/AnimAIverse.git
cd AnimAIverse

# Install Python dependencies
pip install -r requirements.txt
```

### Step 2: Configure Environment

Create a `.env` file in the root directory:

```bash
# API Keys (required)
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Optional: Server Configuration
FLASK_ENV=production
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
```

### Step 3: Run Locally

**Option A: Command Line Interface**
```bash
python animai.py
```

**Option B: On-The-Go Mobile Web App**
```bash
python app_on_the_go.py
```

Access at: `http://localhost:5000`

---

## Production Deployment Options

### Option 1: Heroku (Easiest - Free Tier Available)

**Step 1: Install Heroku CLI**
```bash
# macOS
brew tap heroku/brew && brew install heroku

# Windows
# Download from: https://devcenter.heroku.com/articles/heroku-cli

# Linux
curl https://cli-assets.heroku.com/install.sh | sh
```

**Step 2: Deploy**
```bash
# Login to Heroku
heroku login

# Create app
heroku create your-animaiverse-app

# Set environment variables
heroku config:set OPENAI_API_KEY=your_key_here
heroku config:set ANTHROPIC_API_KEY=your_key_here

# Deploy
git push heroku main

# Open app
heroku open
```

**Step 3: Scale (if needed)**
```bash
# Scale to multiple dynos for better performance
heroku ps:scale web=2

# Upgrade to professional dyno for better performance
heroku dyno:type professional
```

---

### Option 2: AWS (Amazon Web Services)

**Using AWS Elastic Beanstalk**

**Step 1: Install AWS EB CLI**
```bash
pip install awsebcli
```

**Step 2: Initialize and Deploy**
```bash
# Initialize Elastic Beanstalk
eb init -p python-3.11 animaiverse-app --region us-east-1

# Create environment
eb create animaiverse-production

# Set environment variables
eb setenv OPENAI_API_KEY=your_key_here ANTHROPIC_API_KEY=your_key_here

# Deploy updates
eb deploy

# Open in browser
eb open
```

**Step 3: Configure Auto-Scaling**
```bash
# Edit .ebextensions/autoscaling.config
eb config
```

---

### Option 3: Google Cloud Platform (GCP)

**Using Google App Engine**

**Step 1: Install Google Cloud SDK**
```bash
# macOS
brew install google-cloud-sdk

# Windows/Linux
# Download from: https://cloud.google.com/sdk/docs/install
```

**Step 2: Create app.yaml**
```yaml
runtime: python311

env_variables:
  OPENAI_API_KEY: "your_key_here"
  ANTHROPIC_API_KEY: "your_key_here"

instance_class: F2
automatic_scaling:
  min_instances: 1
  max_instances: 10
```

**Step 3: Deploy**
```bash
# Initialize GCP
gcloud init

# Deploy
gcloud app deploy

# Open app
gcloud app browse
```

---

### Option 4: Microsoft Azure

**Using Azure App Service**

**Step 1: Install Azure CLI**
```bash
# macOS
brew install azure-cli

# Windows/Linux
# Download from: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli
```

**Step 2: Deploy**
```bash
# Login
az login

# Create resource group
az group create --name AnimAIverseRG --location eastus

# Create app service plan
az appservice plan create --name AnimAIversePlan --resource-group AnimAIverseRG --sku B1 --is-linux

# Create web app
az webapp create --resource-group AnimAIverseRG --plan AnimAIversePlan --name your-animaiverse-app --runtime "PYTHON:3.11"

# Configure environment variables
az webapp config appsettings set --resource-group AnimAIverseRG --name your-animaiverse-app --settings OPENAI_API_KEY=your_key ANTHROPIC_API_KEY=your_key

# Deploy
az webapp up --name your-animaiverse-app --resource-group AnimAIverseRG
```

---

### Option 5: DigitalOcean

**Using App Platform**

**Step 1: Install doctl**
```bash
# macOS
brew install doctl

# Linux
snap install doctl
```

**Step 2: Deploy**
```bash
# Authenticate
doctl auth init

# Create app
doctl apps create --spec .do/app.yaml

# Or use the web interface at: https://cloud.digitalocean.com/apps
```

---

## Docker Deployment

### Using Docker Container

**Step 1: Build Docker Image**
```bash
docker build -t animaiverse:latest .
```

**Step 2: Run Container**
```bash
docker run -d \
  -p 5000:5000 \
  -e OPENAI_API_KEY=your_key \
  -e ANTHROPIC_API_KEY=your_key \
  --name animaiverse \
  animaiverse:latest
```

**Step 3: Using Docker Compose**
```bash
docker-compose up -d
```

---

## Environment Configuration

### Required Environment Variables

```bash
# AI Service API Keys (Required)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Server Configuration (Optional)
FLASK_ENV=production          # development or production
FLASK_HOST=0.0.0.0           # Host to bind to
FLASK_PORT=5000              # Port to run on
FLASK_DEBUG=False            # Set to True only for development

# Performance Tuning (Optional)
MAX_WORKERS=4                # Number of worker processes
TIMEOUT=300                  # Request timeout in seconds
```

### Configuration Files

**config/config.yaml** - Main configuration
```yaml
language:
  default: "en"
  fallback_to_default: true

agents:
  writer:
    model: "gpt-4"
    temperature: 0.8
  graphics:
    model: "gpt-4"
    temperature: 0.7

adaptive_learning:
  enabled: true
  xp_per_quality_point: 100
  xp_required_per_level: 1000
```

---

## Monitoring & Scaling

### Health Checks

The app includes built-in health check endpoints:

```bash
# Check if app is running
curl http://your-app-url/api/health

# Check system status
curl http://your-app-url/api/evolution
```

### Performance Monitoring

**Option 1: Application Performance Monitoring (APM)**

```bash
# Install New Relic
pip install newrelic

# Configure
export NEW_RELIC_LICENSE_KEY=your_key
newrelic-admin run-program python app_on_the_go.py
```

**Option 2: Prometheus + Grafana**

```bash
# Add prometheus_flask_exporter
pip install prometheus-flask-exporter

# Metrics available at /metrics
```

### Auto-Scaling Configuration

**Heroku Auto-Scaling**
```bash
# Scale based on response time
heroku autoscale:enable web --min 1 --max 10 --p95 500ms
```

**AWS Auto-Scaling**
```yaml
# .ebextensions/autoscaling.config
option_settings:
  - namespace: aws:autoscaling:asg
    option_name: MinSize
    value: 1
  - namespace: aws:autoscaling:asg
    option_name: MaxSize
    value: 10
```

**GCP Auto-Scaling**
```yaml
automatic_scaling:
  min_instances: 1
  max_instances: 10
  target_cpu_utilization: 0.65
```

### Load Balancing

For high-traffic deployments:

```bash
# AWS Application Load Balancer
aws elbv2 create-load-balancer \
  --name animaiverse-lb \
  --subnets subnet-xxx subnet-yyy \
  --security-groups sg-xxx

# GCP Load Balancer
gcloud compute forwarding-rules create animaiverse-lb \
  --global \
  --target-http-proxy=animaiverse-proxy \
  --ports=80
```

---

## Database Configuration (Optional)

For production deployments with persistent storage:

### PostgreSQL Setup

```bash
# Heroku Postgres
heroku addons:create heroku-postgresql:hobby-dev

# AWS RDS
aws rds create-db-instance \
  --db-instance-identifier animaiverse-db \
  --db-instance-class db.t3.micro \
  --engine postgres

# Connection string
DATABASE_URL=postgresql://user:pass@host:5432/animaiverse
```

---

## Security Best Practices

### 1. API Key Management

```bash
# Use environment variables (never commit keys)
export OPENAI_API_KEY=sk-...

# Or use secret management services
aws secretsmanager create-secret --name animaiverse/openai-key
gcloud secrets create openai-key --data-file=-
```

### 2. HTTPS/SSL

```bash
# Heroku (automatic)
heroku certs:auto:enable

# AWS Certificate Manager
aws acm request-certificate --domain-name animaiverse.yourdomain.com

# Let's Encrypt (self-hosted)
certbot --nginx -d animaiverse.yourdomain.com
```

### 3. Rate Limiting

```python
# Add to app_on_the_go.py
from flask_limiter import Limiter

limiter = Limiter(
    app,
    default_limits=["100 per hour", "20 per minute"]
)
```

---

## Troubleshooting

### Common Issues

**Issue: Port Already in Use**
```bash
# Find and kill process
lsof -ti:5000 | xargs kill -9

# Or use different port
export FLASK_PORT=8080
```

**Issue: Memory Error**
```bash
# Increase memory limit (Docker)
docker run -m 2g animaiverse:latest

# Heroku
heroku dyno:resize web=standard-2x
```

**Issue: Slow Response Times**
```bash
# Check logs
heroku logs --tail

# Scale horizontally
heroku ps:scale web=3
```

---

## Production Checklist

Before deploying to production:

- [ ] Set `FLASK_ENV=production`
- [ ] Configure API keys via environment variables
- [ ] Enable HTTPS/SSL
- [ ] Set up monitoring and logging
- [ ] Configure auto-scaling
- [ ] Set up backup for memory/learning files
- [ ] Test health check endpoints
- [ ] Configure rate limiting
- [ ] Set up error tracking (Sentry, Rollbar)
- [ ] Document deployment process for team
- [ ] Set up CI/CD pipeline (optional)

---

## Support

For deployment issues:
- Check logs: `heroku logs --tail` or equivalent
- Review error messages in browser console
- Check API key configuration
- Verify all dependencies are installed

For questions, open an issue on GitHub: https://github.com/Jayc82/AnimAIverse/issues

---

## Quick Start Summary

**Fastest deployment (Heroku):**
```bash
pip install -r requirements.txt
heroku create your-app-name
heroku config:set OPENAI_API_KEY=your_key ANTHROPIC_API_KEY=your_key
git push heroku main
heroku open
```

**Local testing:**
```bash
pip install -r requirements.txt
export OPENAI_API_KEY=your_key
export ANTHROPIC_API_KEY=your_key
python app_on_the_go.py
# Visit http://localhost:5000
```

Your AnimAIverse is now deployed and ready to create revolutionary animations! 🚀
