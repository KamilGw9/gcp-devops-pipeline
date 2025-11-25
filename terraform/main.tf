# terraform/main.tf

# ============================================
# 1. VPC - Sieć prywatna
# ============================================

resource "google_compute_network" "vpc" {
  name                    = "${var.project_id}-vpc"
  auto_create_subnetworks = false  # Sami stworzymy subnety
}

resource "google_compute_subnetwork" "subnet" {
  name          = "${var.project_id}-subnet"
  ip_cidr_range = "10.0.0.0/16"  # Zakres IP: 10.0.0.1 - 10.0.255.254
  region        = var.region
  network       = google_compute_network.vpc.name
  
  # Zakresy IP dla Kubernetes
  secondary_ip_range {
    range_name    = "pods-range"
    ip_cidr_range = "10.1.0.0/16"  # IP dla podów
  }
  
  secondary_ip_range {
    range_name    = "services-range"
    ip_cidr_range = "10.2.0.0/16"  # IP dla serwisów
  }
}

# ============================================
# 2. GKE - Klaster Kubernetes
# ============================================

resource "google_container_cluster" "primary" {
  name     = var.cluster_name
  location = var.zone
  
  # Usuwamy domyślny node pool (stworzymy własny)
  remove_default_node_pool = true
  initial_node_count       = 1
  
  # Podłączamy do naszej sieci VPC
  network    = google_compute_network.vpc.name
  subnetwork = google_compute_subnetwork.subnet.name
  
  # Konfiguracja IP dla podów i serwisów
  ip_allocation_policy {
    cluster_secondary_range_name  = "pods-range"
    services_secondary_range_name = "services-range"
  }
}

# Node Pool - faktyczne serwery w klastrze
resource "google_container_node_pool" "primary_nodes" {
  name       = "${var.cluster_name}-node-pool"
  location   = var.zone
  cluster    = google_container_cluster.primary.name
  node_count = var.node_count
  
  node_config {
    machine_type = var.machine_type
    disk_size_gb = 50
    
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
    
    labels = {
      env = "dev"
    }
    
    tags = ["gke-node", var.cluster_name]
  }
}

# ============================================
# 3. Artifact Registry - Magazyn obrazów Docker
# ============================================

resource "google_artifact_registry_repository" "docker_repo" {
  location      = var.region
  repository_id = "docker-repo"
  description   = "Docker repository for container images"
  format        = "DOCKER"
}