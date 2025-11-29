# Monitoring - Prometheus i Grafana

## Przegląd

Ten projekt zawiera kompletny stack monitoringu z Prometheus i Grafana.

### Komponenty:
- **Prometheus**: Zbieranie metryk z aplikacji i klastra Kubernetes
- **Grafana**: Wizualizacja metryk i dashboardy

## Architektura

```
┌─────────────────────────────────────────────────────────┐
│                   Kubernetes Cluster                     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────────────┐     ┌────────────────────┐   │
│  │ data-pipeline-api    │     │   Prometheus       │   │
│  │ (metrics endpoint)   │────→│ (scraping metrics) │   │
│  └──────────────────────┘     └────────────────────┘   │
│                                      │                  │
│                                      ↓                  │
│                              ┌────────────────────┐   │
│                              │     Grafana        │   │
│                              │  (visualization)   │   │
│                              └────────────────────┘   │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Dostęp

### Prometheus
- **URL**: `http://<PROMETHEUS_SERVICE_IP>:9090`
- **Namespace**: `monitoring`

### Grafana
- **URL**: `http://<GRAFANA_SERVICE_IP>:3000`
- **Username**: `admin`
- **Password**: Ustawione w GitHub Secret `GRAFANA_PASSWORD`
- **Namespace**: `monitoring`

## Metryki aplikacji

Aplikacja udostępnia endpoint `/metrics` z metryki Prometheus:

- `app_requests_total` - Całkowita liczba requestów
- `app_request_duration_seconds` - Czas trwania requestów
- `app_transform_operations_total` - Liczba operacji transformacji danych

## Deployment

Monitoring deployowany jest automatycznie przez GitHub Actions:

```bash
# Lokalne deployment
helm install prometheus ./helm/prometheus \
  --namespace monitoring \
  --create-namespace

helm install grafana ./helm/grafana \
  --namespace monitoring \
  --set adminPassword="YOUR_PASSWORD"
```

## Dodanie nowych dashboardów

Dashboardy w Grafanie można dodawać przez UI lub przez ConfigMaps.

## Troubleshooting

### Prometheus nie scrapeuje metryk

```bash
# Sprawdź czy aplikacja ma metrics endpoint
kubectl logs -n default deployment/data-pipeline-api

# Sprawdź Prometheus config
kubectl get configmap -n monitoring prometheus-config -o yaml
```

### Grafana nie widzi Prometheus

```bash
# Sprawdź czy datasource jest skonfigurowany
kubectl get configmap -n monitoring grafana-datasources -o yaml
```

## Dokumentacja

- [Prometheus Docs](https://prometheus.io/docs/)
- [Grafana Docs](https://grafana.com/docs/)
