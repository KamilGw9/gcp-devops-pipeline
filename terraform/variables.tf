variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region for resources"
  type        = string
  default     = "europe-central2"
}

variable "zone" {
  description = "GCP zone within the region"
  type        = string
  default     = "europe-central2-a"
}

variable "cluster_name" {
  description = "Name of the GKE cluster"
  type        = string
  default     = "devops-cluster"
}

variable "node_count" {
  description = "Number of nodes in the cluster"
  type        = number
  default     = 2
}

variable "machine_type" {
  description = "Machine type for cluster nodes"
  type        = string
  default     = "e2-medium"
}