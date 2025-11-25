# terraform/outputs.tf

# === KLASTER KUBERNETES ===

output "cluster_name" {
  description = "Nazwa klastra GKE"
  value       = google_container_cluster.primary.name
}

output "cluster_endpoint" {
  description = "Endpoint klastra (adres API Kubernetes)"
  value       = google_container_cluster.primary.endpoint
  sensitive   = true  # Ukryj w logach (bezpieczeństwo)
}

output "cluster_location" {
  description = "Lokalizacja klastra"
  value       = google_container_cluster.primary.location
}

# === SIEĆ ===

output "vpc_name" {
  description = "Nazwa sieci VPC"
  value       = google_compute_network.vpc.name
}

output "subnet_name" {
  description = "Nazwa subnetu"
  value       = google_compute_subnetwork.subnet.name
}

# === ARTIFACT REGISTRY ===

output "docker_repo_url" {
  description = "URL do Artifact Registry (tu pushujemy obrazy Docker)"
  value       = "${var.region}-docker.pkg.dev/${var.project_id}/docker-repo"
}