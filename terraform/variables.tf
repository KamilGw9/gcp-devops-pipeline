# terraform/variables.tf

# === PODSTAWOWE ===

variable "project_id" {
  description = "ID projektu w Google Cloud"
  type        = string
}

variable "region" {
  description = "Region GCP gdzie tworzymy zasoby"
  type        = string
  default     = "europe-central2"  # Warszawa - najbliżej nas!
}

variable "zone" {
  description = "Strefa w regionie (a, b, lub c)"
  type        = string
  default     = "europe-central2-a"
}

# === KUBERNETES (GKE) ===

variable "cluster_name" {
  description = "Nazwa klastra Kubernetes"
  type        = string
  default     = "devops-cluster"
}

variable "node_count" {
  description = "Liczba nodów (serwerów) w klastrze"
  type        = number
  default     = 2  # 2 nody = dobry balans cena/wydajność
}

variable "machine_type" {
  description = "Typ maszyny dla nodów"
  type        = string
  default     = "e2-medium"  # 2 vCPU, 4GB RAM - tani ale wystarczający
}