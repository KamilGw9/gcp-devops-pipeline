# VPC Network

resource "google_compute_network" "vpc" {
  name                    = "${var.project_id}-vpc"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "subnet" {
  name          = "${var.project_id}-subnet"
  ip_cidr_range = "10.0.0.0/16"
  region        = var.region
  network       = google_compute_network.vpc.name
  
  secondary_ip_range {
    range_name    = "pods-range"
    ip_cidr_range = "10.1.0.0/16"
  }
  
  secondary_ip_range {
    range_name    = "services-range"
    ip_cidr_range = "10.2.0.0/16"
  }
}

# GKE Cluster

resource "google_container_cluster" "primary" {
  name     = var.cluster_name
  location = var.zone
  
  remove_default_node_pool = true
  initial_node_count       = 1
  
  network    = google_compute_network.vpc.name
  subnetwork = google_compute_subnetwork.subnet.name
  
  ip_allocation_policy {
    cluster_secondary_range_name  = "pods-range"
    services_secondary_range_name = "services-range"
  }
}

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

# Artifact Registry

resource "google_artifact_registry_repository" "docker_repo" {
  location      = var.region
  repository_id = "docker-repo"
  description   = "Docker repository for container images"
  format        = "DOCKER"
}