# Crypto Tracker API

[![CI Pipeline](https://github.com/KamilGw9/gcp-devops-pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/KamilGw9/gcp-devops-pipeline/actions/workflows/ci.yml)

A small Flask API that fetches crypto prices from CoinGecko and stores a portfolio and price alerts in PostgreSQL. It runs on GKE, with infrastructure in Terraform and deployments through GitHub Actions.

The app itself is deliberately simple. The point of the project is everything around it: infrastructure, networking, TLS, network policies, monitoring and CI/CD on GCP.

## Architecture

```
            HTTPS (Let's Encrypt, cert-manager)
                        │
                ┌───────▼────────┐
                │ NGINX Ingress  │
                └───────┬────────┘
                        │
              ┌─────────▼──────────┐
              │ data-pipeline-api  │  Deployment, 2 replicas (gunicorn)
              └──┬───────┬──────┬──┘
                 │       │      │
          ┌──────▼─┐ ┌───▼────┐ └──► CoinGecko API
          │ Redis  │ │Postgres│
          │ cache  │ │        │
          └────────┘ └────────┘

   Prometheus + Grafana (kube-prometheus-stack), namespace: monitoring
```

- **GKE**: zonal cluster in `europe-central2-a`, 2 × `e2-medium` nodes, VPC-native networking
- **Terraform**: VPC, subnet, GKE cluster and node pool, Artifact Registry. State is kept in a GCS bucket.
- **Redis**: caches CoinGecko responses (60 s for a single coin, 5 min for the top 10). If Redis is down, the app still works without the cache.
- **PostgreSQL**: stores the portfolio and alerts (SQLAlchemy). Tables are created on startup.
- **Redis and PostgreSQL** are installed from the Bitnami Helm charts, not Terraform.

## Repository layout

```
app/                      Flask app, tests, Dockerfile
terraform/                GCP infrastructure
k8s/
  deployment.yaml         Deployment + Service
  ingress.yaml            NGINX Ingress with TLS
  cluster-issuer.yaml     cert-manager ClusterIssuer (Let's Encrypt)
  network-policies/       default deny + allow rules for the app and Redis
.github/workflows/
  ci.yml                  tests on push / PR
  deploy.yaml             build, push and deploy on push to main
MONITORING.md             monitoring notes (in Polish)
```

## API

| Method | Path                  | Description                                   |
|--------|-----------------------|-----------------------------------------------|
| GET    | `/`                   | Service name and version                      |
| GET    | `/health`             | DB and Redis status                           |
| GET    | `/metrics`            | Prometheus metrics                            |
| GET    | `/api/crypto/top10`   | Top 10 coins by market cap (USD)              |
| GET    | `/api/crypto/<coin>`  | Price in USD/EUR/PLN, 24h change, market cap  |
| GET    | `/api/portfolio`      | Holdings valued at current prices (USD, PLN)  |
| POST   | `/api/portfolio/add`  | `{"coin": "bitcoin", "amount": 0.5}`          |
| GET    | `/api/alerts`         | List alerts                                   |
| POST   | `/api/alerts`         | `{"coin": "bitcoin", "target_price": 50000, "direction": "above"}` |

`<coin>` is a CoinGecko ID, for example `bitcoin` or `ethereum`.

```bash
curl https://34-116-189-129.nip.io/api/crypto/bitcoin

curl -X POST https://34-116-189-129.nip.io/api/portfolio/add \
  -H "Content-Type: application/json" \
  -d '{"coin": "bitcoin", "amount": 0.5}'
```

Alerts are only stored for now. Nothing checks them against current prices yet.

## Configuration

| Variable         | Default               | Notes                                    |
|------------------|-----------------------|------------------------------------------|
| `DB_HOST`        | `postgres-postgresql` |                                          |
| `DB_USER`        | `postgres`            | from `postgres-secret` in the cluster    |
| `DB_PASSWORD`    | `postgres`            | from `postgres-secret` in the cluster    |
| `DB_NAME`        | `postgres`            |                                          |
| `DATABASE_URL`   | built from the above  | overrides the `DB_*` variables           |
| `REDIS_HOST`     | `redis-master`        |                                          |
| `REDIS_PORT`     | `6379`                |                                          |
| `REDIS_PASSWORD` | empty                 | from `redis-secret` in the cluster       |
| `APP_VERSION`    | `2.1.0`               | returned by `/`                          |
| `SKIP_DB_INIT`   | unset                 | `true` skips `create_all()` (used in tests) |

## Running locally

```bash
docker run -d --name postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 postgres:14
docker run -d --name redis -p 6379:6379 redis:7

cd app
pip install -r requirements.txt
DB_HOST=localhost REDIS_HOST=localhost python main.py   # http://localhost:8080
```

Tests use in-memory SQLite, so they don't need Postgres or Redis. Two of them call the real CoinGecko API.

```bash
cd app && python -m pytest -v
```

## Deploying from scratch

Requirements: gcloud, Terraform >= 1.0, kubectl, Helm 3, Docker.

**1. Infrastructure**

The GCS bucket for the Terraform state (`terraform/providers.tf`) has to exist before `init`.

```bash
cd terraform
terraform init
terraform apply -var="project_id=YOUR_PROJECT_ID"
gcloud container clusters get-credentials devops-cluster --zone europe-central2-a
```

**2. Cluster add-ons**

```bash
# cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml
kubectl apply -f k8s/cluster-issuer.yaml

# NGINX Ingress
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm upgrade --install ingress-nginx ingress-nginx/ingress-nginx \
  -n ingress-nginx --create-namespace

# PostgreSQL and Redis
helm repo add bitnami https://charts.bitnami.com/bitnami
helm upgrade --install postgres bitnami/postgresql \
  --set auth.password=CHANGE_ME --set auth.database=postgres
helm upgrade --install redis bitnami/redis --set auth.password=CHANGE_ME

kubectl create secret generic postgres-secret \
  --from-literal=username=postgres --from-literal=password=CHANGE_ME
kubectl create secret generic redis-secret --from-literal=password=CHANGE_ME
```

**3. Application**

```bash
kubectl apply -f k8s/network-policies/
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/ingress.yaml
```

The hostname in `k8s/ingress.yaml` is a nip.io address built from the ingress controller's external IP. Update it for a new cluster.

After this, pushing to `main` builds and deploys the app.

## CI/CD

**`ci.yml`** runs on pushes to `main`, `develop` and `feature/*`, and on PRs to `main` and `develop`. It installs dependencies and runs pytest.

**`deploy.yaml`** runs on push to `main`:

1. Authenticates to GCP with Workload Identity Federation, so no service account key is stored in GitHub.
2. Builds the image and pushes it to Artifact Registry, tagged with the commit SHA and `latest`.
3. Installs or updates `kube-prometheus-stack` with Helm. The Grafana password comes from the `GRAFANA_PASSWORD` secret.
4. Runs `kubectl set image` and waits for the rollout to finish.

Branching: feature branches go into `develop`, and `develop` is merged into `main` for a release.

## Security

- `default-deny-all` blocks all ingress and egress in the `default` namespace.
- The app accepts traffic only from the `ingress-nginx` and `monitoring` namespaces. It can connect out only to Redis, Postgres, DNS, and public IPs on port 443.
- Redis accepts connections only from the app pods.
- TLS is terminated at the ingress with a Let's Encrypt certificate, and HTTP redirects to HTTPS.
- The container runs as a non-root user. CPU and memory requests and limits are set.
- Database and Redis passwords are stored in Kubernetes secrets.

## Monitoring

`kube-prometheus-stack` runs in the `monitoring` namespace. The app exposes `/metrics` through `prometheus_client`. Pods have `prometheus.io/*` annotations, but no ServiceMonitor is defined yet.

```bash
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80   # login: admin
```

More details are in [MONITORING.md](MONITORING.md).

## Known issues / TODO

- Postgres has no NetworkPolicy of its own. With `default-deny-all` in place, it will block traffic until one is added.
- `app_requests_total` is only incremented on `/api/crypto/<coin>`, and `app_request_duration_seconds` is never recorded.
- The Workload Identity pool, provider and service account were created manually. They should be moved into Terraform.
- The deploy uses `:latest` instead of the SHA tag, so a rollback means retagging the image.
- CI runs Python 3.10, but the Docker image uses 3.11.
- No authentication. The portfolio is shared by everyone who calls the API.
- The alerts don't trigger anything yet.

## Author

Kamil Gw · [@KamilGw9](https://github.com/KamilGw9)
