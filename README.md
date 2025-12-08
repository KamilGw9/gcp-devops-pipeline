# 🚀 Crypto Tracker API

![Google Cloud](https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
![NGINX](https://img.shields.io/badge/NGINX-009639?style=for-the-badge&logo=nginx&logoColor=white)
![cert-manager](https://img.shields.io/badge/cert--manager-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)
![Helm](https://img.shields.io/badge/Helm-0F1689?style=for-the-badge&logo=helm&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white)

A production-ready cryptocurrency tracking API demonstrating modern cloud-native practices on Google Cloud Platform. This project showcases real-time crypto price tracking, portfolio management, Infrastructure as Code, containerization, orchestration, monitoring, and CI/CD automation with enterprise-grade security.

---

## 📋 Table of Contents

- [Architecture Overview](#-architecture-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [API Endpoints](#-api-endpoints)
- [Environment Variables](#-environment-variables)
- [Security](#-security)
- [Monitoring](#-monitoring)
- [Quick Start](#-quick-start)
- [GitFlow Workflow](#-gitflow-workflow)
- [CI/CD Pipeline](#-cicd-pipeline)
- [License](#-license)
- [Author](#-author)

---

## 🏗 Architecture Overview

The Crypto Tracker API is built with a modern microservices architecture:

```
┌─────────────────────────────────────────────────────────────────┐
│                      Internet / Users                           │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ↓
                    ┌────────────────┐
                    │ NGINX Ingress  │  ← TLS/SSL (Let's Encrypt)
                    │   Controller   │
                    └────────┬───────┘
                             │
                             ↓
              ┌──────────────────────────────┐
              │   LoadBalancer Service       │
              └──────────────┬───────────────┘
                             │
                    ┌────────┴────────┐
                    │                 │
            ┌───────▼──────┐  ┌──────▼───────┐
            │ Flask App    │  │  Flask App   │  (2 replicas)
            │ Pod 1        │  │  Pod 2       │
            └──┬────────┬──┘  └──┬────────┬──┘
               │        │        │        │
        ┌──────▼─┐  ┌──▼────────▼──┐  ┌──▼─────────┐
        │ Redis  │  │  PostgreSQL  │  │ CoinGecko  │
        │ Cache  │  │  Database    │  │ API        │
        └────────┘  └──────────────┘  └────────────┘
```

**Key Components:**
- **Flask Application**: Python web API with SQLAlchemy ORM for data persistence
- **PostgreSQL**: Primary database for portfolio data and price alerts
- **Redis**: Caching layer for API responses (60s for prices, 5min for top 10)
- **CoinGecko API**: Real-time cryptocurrency price data integration
- **Kubernetes**: Container orchestration with 2 replicas for high availability
- **NGINX Ingress**: Load balancing and SSL/TLS termination
- **cert-manager**: Automatic SSL/TLS certificate management with Let's Encrypt
- **Network Policies**: Zero-trust security with default deny and explicit allow rules
- **Prometheus + Grafana**: Full observability and metrics visualization

---

## ✨ Features

### 🪙 Real-time Crypto Prices
- Integration with CoinGecko API for live cryptocurrency data
- Multi-currency support: USD, EUR, PLN
- 24-hour price change tracking
- Market capitalization data

### 💼 Portfolio Management
- Persistent storage with PostgreSQL backend
- Add cryptocurrencies to your portfolio
- Real-time portfolio valuation
- Track holdings across multiple coins

### 🔔 Price Alerts
- Set target price notifications
- Configure alerts for price movements (above/below thresholds)
- Persistent alert storage

### ⚡ Performance & Caching
- Redis caching layer for optimal performance
- 60-second cache for individual price data
- 5-minute cache for top 10 cryptocurrencies
- Reduced API calls and faster response times

### 🔒 Enterprise Security
- Network policies with default deny rules
- TLS/SSL encryption with Let's Encrypt certificates
- Kubernetes secrets for sensitive credentials
- Resource limits to prevent resource exhaustion

### 📊 Observability
- Prometheus metrics endpoint
- Grafana dashboards for visualization
- Health checks with DB and Redis status
- Request duration and rate tracking

---

## 🛠 Tech Stack

| Category | Technology |
|----------|------------|
| ☁️ **Cloud** | Google Cloud Platform (GKE, Artifact Registry, VPC) |
| 🏗️ **IaC** | Terraform |
| 🐍 **App** | Python 3.10, Flask |
| 🗄️ **Database** | PostgreSQL, SQLAlchemy ORM |
| ⚡ **Cache** | Redis |
| 🐳 **Containerization** | Docker |
| ☸️ **Orchestration** | Kubernetes |
| 🌐 **Ingress** | NGINX Ingress Controller |
| 🔐 **Certificates** | cert-manager, Let's Encrypt |
| 📦 **Package Manager** | Helm |
| 📊 **Monitoring** | Prometheus, Grafana |
| 🔄 **CI/CD** | GitHub Actions |
| 📝 **Version Control** | Git with GitFlow |

---

## 📁 Project Structure

```
├── app/                  # Flask application
│   ├── main.py
│   ├── test_app.py
│   ├── Dockerfile
│   └── requirements.txt
├── terraform/            # Infrastructure as Code
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── providers.tf
├── k8s/                  # Kubernetes manifests
│   ├── deployment.yaml
│   ├── ingress.yaml              # NGINX Ingress with TLS
│   ├── cluster-issuer.yaml       # cert-manager configuration
│   └── network-policies/         # Security policies
│       ├── app-policy.yaml
│       ├── redis-policy.yaml
│       └── default-deny.yaml
├── .github/workflows/    # CI/CD pipelines
│   ├── ci.yml            # Continuous Integration
│   └── deploy.yaml       # Continuous Deployment
└── MONITORING.md         # Monitoring documentation
```

---

## 🔌 API Endpoints

The Crypto Tracker API provides the following endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API information and version |
| `GET` | `/health` | Health check (DB + Redis status) |
| `GET` | `/metrics` | Prometheus metrics endpoint |
| `GET` | `/api/crypto/top10` | Get top 10 cryptocurrencies by market cap |
| `GET` | `/api/crypto/<coin>` | Get current price for specific cryptocurrency |
| `POST` | `/api/portfolio/add` | Add cryptocurrency to portfolio |
| `GET` | `/api/portfolio` | Get portfolio with current valuations |
| `GET` | `/api/alerts` | View all price alerts |
| `POST` | `/api/alerts` | Create new price alert |

### Example Requests

**Get API Info:**
```bash
curl https://34-116-189-129.nip.io/
```

**Health Check:**
```bash
curl https://34-116-189-129.nip.io/health
```

**Get Top 10 Cryptocurrencies:**
```bash
curl https://34-116-189-129.nip.io/api/crypto/top10
```

**Get Bitcoin Price:**
```bash
curl https://34-116-189-129.nip.io/api/crypto/bitcoin
```

**Add to Portfolio:**
```bash
curl -X POST https://34-116-189-129.nip.io/api/portfolio/add \
  -H "Content-Type: application/json" \
  -d '{"coin": "bitcoin", "amount": 0.5}'
```

**View Portfolio:**
```bash
curl https://34-116-189-129.nip.io/api/portfolio
```

**Create Price Alert:**
```bash
curl -X POST https://34-116-189-129.nip.io/api/alerts \
  -H "Content-Type: application/json" \
  -d '{"coin": "bitcoin", "target_price": 50000, "direction": "above"}'
```

**View All Alerts:**
```bash
curl https://34-116-189-129.nip.io/api/alerts
```

---

## 🔐 Environment Variables

The application requires the following environment variables:

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `APP_VERSION` | Application version | `2.1.0` | No |
| `REDIS_HOST` | Redis server hostname | `redis-master` | Yes |
| `REDIS_PORT` | Redis server port | `6379` | No |
| `REDIS_PASSWORD` | Redis authentication password | - | Yes (in production) |
| `DB_HOST` | PostgreSQL server hostname | `postgres-postgresql` | Yes |
| `DB_USER` | PostgreSQL username | `postgres` | Yes |
| `DB_PASSWORD` | PostgreSQL password | - | Yes |
| `DB_NAME` | PostgreSQL database name | `postgres` | Yes |
| `SKIP_DB_INIT` | Skip automatic table creation | `false` | No |

### Kubernetes Secrets

Sensitive credentials are stored as Kubernetes secrets:

```bash
# Create Redis secret
kubectl create secret generic redis-secret \
  --from-literal=password=YOUR_REDIS_PASSWORD

# Create PostgreSQL secret
kubectl create secret generic postgres-secret \
  --from-literal=username=postgres \
  --from-literal=password=YOUR_POSTGRES_PASSWORD
```

---

## 🔒 Security

This project implements enterprise-grade security practices:

### Network Policies
- **Default Deny**: All ingress traffic denied by default
- **App Policy**: Explicit allow rules for application traffic
- **Redis Policy**: Restricted access to Redis from application pods only
- **PostgreSQL Policy**: Database access restricted to application pods

### TLS/SSL Encryption
- NGINX Ingress Controller with TLS termination
- Let's Encrypt certificates via cert-manager
- Automatic certificate renewal
- HTTPS enforcement with automatic redirect

### Secrets Management
- Kubernetes secrets for sensitive credentials
- Redis and PostgreSQL passwords stored securely
- No hardcoded credentials in code or configuration

### Resource Limits
- Memory limits: 128Mi (request) to 256Mi (limit)
- CPU limits: 100m (request) to 200m (limit)
- Prevents resource exhaustion attacks
- Ensures fair resource allocation

### Health Probes
- **Liveness Probe**: Automatically restarts unhealthy pods
- **Readiness Probe**: Ensures traffic only to ready pods
- Both probes check `/health` endpoint with DB and Redis status

---

## 📊 Monitoring

This project includes a complete monitoring stack with Prometheus and Grafana.

### Components

| Component | Purpose |
|-----------|---------|
| **Prometheus** | Metrics collection and storage from application and Kubernetes cluster |
| **Grafana** | Visualization and dashboards for metrics analysis |
| **kube-prometheus-stack** | Complete monitoring solution with pre-configured dashboards |

### Application Metrics

The application exposes the following Prometheus metrics at `/metrics`:

- `app_requests_total{method, endpoint}` - Total number of requests by HTTP method and endpoint
- `app_request_duration_seconds` - Request duration histogram for performance tracking

### Deployment

The monitoring stack is deployed using the official Prometheus Community Helm chart:

```bash
# Add Prometheus Community Helm repository
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Deploy monitoring stack
helm upgrade --install monitoring prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace \
  --set grafana.adminPassword="YOUR_SECURE_PASSWORD" \
  --set prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues=false
```

### Access Monitoring Services

```bash
# Get Prometheus service
kubectl get svc -n monitoring | grep prometheus

# Get Grafana service  
kubectl get svc -n monitoring | grep grafana

# Port forward Grafana to access locally
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
# Access at http://localhost:3000 (username: admin)
```

📖 For detailed monitoring documentation, see [MONITORING.md](MONITORING.md)

---

## 🚀 Quick Start

### Prerequisites

- Google Cloud Platform account
- [gcloud CLI](https://cloud.google.com/sdk/docs/install) installed and configured
- [Terraform](https://www.terraform.io/downloads) >= 1.0.0
- [Docker](https://docs.docker.com/get-docker/) installed
- [kubectl](https://kubernetes.io/docs/tasks/tools/) installed
- [Helm](https://helm.sh/docs/intro/install/) >= 3.0 installed

### Infrastructure Deployment

1. **Clone the repository:**
   ```bash
   git clone https://github.com/KamilGw9/gcp-devops-pipeline.git
   cd gcp-devops-pipeline
   ```

2. **Set up GCP authentication:**
   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   ```

3. **Deploy infrastructure with Terraform:**
   ```bash
   cd terraform
   terraform init
   terraform plan -var="project_id=YOUR_PROJECT_ID"
   terraform apply -var="project_id=YOUR_PROJECT_ID"
   ```

4. **Configure kubectl:**
   ```bash
   gcloud container clusters get-credentials devops-cluster --zone europe-central2-a
   ```

### Dependencies Setup

#### 1. Install cert-manager (for TLS certificates)

```bash
# Install cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml

# Wait for cert-manager to be ready
kubectl wait --for=condition=ready pod -l app.kubernetes.io/instance=cert-manager -n cert-manager --timeout=300s

# Apply cluster issuer for Let's Encrypt
kubectl apply -f k8s/cluster-issuer.yaml
```

#### 2. Install NGINX Ingress Controller

```bash
# Add NGINX Ingress Helm repository
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

# Install NGINX Ingress Controller
helm upgrade --install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx \
  --create-namespace \
  --set controller.service.type=LoadBalancer
```

#### 3. Deploy PostgreSQL

```bash
# Add Bitnami Helm repository
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# Install PostgreSQL
helm upgrade --install postgres bitnami/postgresql \
  --namespace default \
  --set auth.username=postgres \
  --set auth.password=YOUR_POSTGRES_PASSWORD \
  --set auth.database=postgres

# Create PostgreSQL secret for application
kubectl create secret generic postgres-secret \
  --from-literal=username=postgres \
  --from-literal=password=YOUR_POSTGRES_PASSWORD
```

#### 4. Deploy Redis

```bash
# Install Redis
helm upgrade --install redis bitnami/redis \
  --namespace default \
  --set auth.password=YOUR_REDIS_PASSWORD

# Create Redis secret for application
kubectl create secret generic redis-secret \
  --from-literal=password=YOUR_REDIS_PASSWORD
```

### Application Deployment

1. **Build the Docker image:**
   ```bash
   cd app
   docker build -t crypto-tracker-api:v1 .
   ```

2. **Push to Artifact Registry:**
   ```bash
   gcloud auth configure-docker europe-central2-docker.pkg.dev
   docker tag crypto-tracker-api:v1 europe-central2-docker.pkg.dev/YOUR_PROJECT_ID/docker-repo/data-pipeline-api:latest
   docker push europe-central2-docker.pkg.dev/YOUR_PROJECT_ID/docker-repo/data-pipeline-api:latest
   ```

3. **Apply Network Policies:**
   ```bash
   kubectl apply -f k8s/network-policies/
   ```

4. **Deploy to Kubernetes:**
   ```bash
   kubectl apply -f k8s/deployment.yaml
   kubectl apply -f k8s/ingress.yaml
   ```

5. **Deploy Monitoring Stack:**
   ```bash
   helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
   helm repo update
   
   helm upgrade --install monitoring prometheus-community/kube-prometheus-stack \
     --namespace monitoring \
     --create-namespace \
     --set grafana.adminPassword="YOUR_GRAFANA_PASSWORD" \
     --set prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues=false
   ```

6. **Verify deployment:**
   ```bash
   # Check application pods
   kubectl get pods -l app=data-pipeline-api
   
   # Check services
   kubectl get svc
   
   # Check ingress
   kubectl get ingress
   
   # Get Ingress external IP
   kubectl get ingress crypto-tracker-ingress -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
   ```

### Local Development

Run the application locally with dependencies:

```bash
# Start PostgreSQL (using Docker)
docker run --name postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:14

# Start Redis (using Docker)
docker run --name redis -p 6379:6379 -d redis:7

# Install Python dependencies
cd app
pip install -r requirements.txt

# Set environment variables
export DB_HOST=localhost
export DB_USER=postgres
export DB_PASSWORD=postgres
export DB_NAME=postgres
export REDIS_HOST=localhost
export REDIS_PORT=6379
export REDIS_PASSWORD=""

# Run the application
python main.py
```

Run tests:
```bash
cd app
python -m pytest test_app.py -v
```

---

## 🌿 GitFlow Workflow

This project follows the GitFlow branching strategy:

| Branch | Purpose |
|--------|---------|
| `main` | Production-ready code. Protected branch with required reviews. |
| `develop` | Integration branch for features. Latest development changes. |
| `feature/*` | Feature branches for new development work. |

### Workflow

1. Create a feature branch from `develop`:
   ```bash
   git checkout develop
   git checkout -b feature/my-new-feature
   ```

2. Make changes and commit:
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

3. Push and create a Pull Request to `develop`:
   ```bash
   git push origin feature/my-new-feature
   ```

4. After review and merge to `develop`, create PR to `main` for release.

---

## 🔄 CI/CD Pipeline

The project uses GitHub Actions for automated CI/CD with two workflows:

### CI Workflow (`.github/workflows/ci.yml`)

**Triggers:**
- **Push** to `main`, `develop`, and `feature/*` branches
- **Pull Requests** to `main` and `develop` branches

**Steps:**
1. **Checkout Code** - Fetches the latest code from the repository
2. **Setup Python** - Configures Python 3.10 environment
3. **Install Dependencies** - Installs required Python packages
4. **Run Tests** - Executes pytest with verbose output

### Deploy Workflow (`.github/workflows/deploy.yaml`)

**Triggers:**
- Push to `main` branch

**Steps:**
1. **Build Docker Image** - Creates container image
2. **Push to Artifact Registry** - Uploads image to GCP
3. **Deploy to GKE** - Updates Kubernetes deployment
4. **Deploy Monitoring** - Installs/updates Prometheus and Grafana via Helm

---

## 📄 License

This project is licensed under the MIT License.

```
MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 👤 Author

**Kamil Gw**

- GitHub: [@KamilGw9](https://github.com/KamilGw9)

---

⭐ Star this repository if you find it helpful!