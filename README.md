# 🚀 GCP DevOps Pipeline

![Google Cloud](https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)
![Helm](https://img.shields.io/badge/Helm-0F1689?style=for-the-badge&logo=helm&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white)

A production-ready DevOps pipeline demonstrating modern cloud-native practices on Google Cloud Platform. This project showcases Infrastructure as Code, containerization, orchestration, monitoring, and CI/CD automation.

---

## 📋 Table of Contents

- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [API Endpoints](#-api-endpoints)
- [Monitoring](#-monitoring)
- [Quick Start](#-quick-start)
- [GitFlow Workflow](#-gitflow-workflow)
- [CI/CD Pipeline](#-cicd-pipeline)
- [License](#-license)
- [Author](#-author)

---

## 🛠 Tech Stack

| Category | Technology |
|----------|------------|
| ☁️ **Cloud** | Google Cloud Platform (GKE, Artifact Registry, VPC) |
| 🏗️ **IaC** | Terraform |
| 🐍 **App** | Python 3.10, Flask |
| 🐳 **Containerization** | Docker |
| ☸️ **Orchestration** | Kubernetes |
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
│   └── deployment.yaml
├── helm/                 # Helm charts
│   ├── prometheus/       # Prometheus monitoring
│   └── grafana/          # Grafana dashboards
└── .github/workflows/    # CI/CD pipelines
    ├── ci.yml            # Continuous Integration
    └── deploy.yaml       # Continuous Deployment
```

---

## 🔌 API Endpoints

The Data Pipeline API provides the following endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Returns API info and available endpoints |
| `GET` | `/health` | Health check for monitoring and load balancers |
| `GET` | `/metrics` | Prometheus metrics endpoint |
| `POST` | `/api/transform` | Transforms incoming data (ETL operations) |
| `GET` | `/api/stats` | Returns statistics for processed records |

### Example Requests

**Get API Info:**
```bash
curl http://localhost:8080/
```

**Health Check:**
```bash
curl http://localhost:8080/health
```

**Transform Data:**
```bash
curl -X POST http://localhost:8080/api/transform \
  -H "Content-Type: application/json" \
  -d '{"name": "john", "age": "30"}'
```

**Get Statistics:**
```bash
curl http://localhost:8080/api/stats
```

---

## 📊 Monitoring

This project includes a complete monitoring stack with Prometheus and Grafana.

### Components

| Component | Purpose |
|-----------|---------|
| **Prometheus** | Metrics collection and storage |
| **Grafana** | Visualization and dashboards |

### Application Metrics

The application exposes the following Prometheus metrics:

- `app_requests_total` - Total number of requests
- `app_request_duration_seconds` - Request duration
- `app_transform_operations_total` - Number of data transformation operations

### Deployment

```bash
# Deploy Prometheus
helm install prometheus ./helm/prometheus \
  --namespace monitoring \
  --create-namespace

# Deploy Grafana
helm install grafana ./helm/grafana \
  --namespace monitoring \
  --set adminPassword="YOUR_PASSWORD"
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
- [Helm](https://helm.sh/docs/intro/install/) installed

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

### Application Deployment

1. **Build the Docker image:**
   ```bash
   cd app
   docker build -t data-pipeline-api:v1 .
   ```

2. **Push to Artifact Registry:**
   ```bash
   gcloud auth configure-docker europe-central2-docker.pkg.dev
   docker tag data-pipeline-api:v1 europe-central2-docker.pkg.dev/YOUR_PROJECT_ID/docker-repo/data-pipeline-api:v1
   docker push europe-central2-docker.pkg.dev/YOUR_PROJECT_ID/docker-repo/data-pipeline-api:v1
   ```

3. **Configure kubectl:**
   ```bash
   gcloud container clusters get-credentials devops-cluster --zone europe-central2-a
   ```

4. **Deploy to Kubernetes:**
   ```bash
   kubectl apply -f k8s/deployment.yaml
   ```

5. **Deploy Monitoring Stack:**
   ```bash
   helm install prometheus ./helm/prometheus --namespace monitoring --create-namespace
   helm install grafana ./helm/grafana --namespace monitoring
   ```

### Local Development

Run the application locally:
```bash
cd app
pip install -r requirements.txt
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

Copyright (c) 2024

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