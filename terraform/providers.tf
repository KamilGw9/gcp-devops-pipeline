# terraform/providers.tf

# Określamy wymaganą wersję Terraform
terraform {
  required_version = ">= 1.0.0"  # Minimum wersja 1.0.0
  
  # Lista providerów których używamy
  required_providers {
    google = {
      source  = "hashicorp/google"  # Skąd pobrać provider
      version = "~> 5.0"             # Wersja 5.x (najnowsza stabilna)
    }
  }
}

# Konfiguracja providera Google
provider "google" {
  project = var.project_id   # ID projektu GCP (z variables.tf)
  region  = var.region       # Region (np. europe-central2 = Warszawa)
}