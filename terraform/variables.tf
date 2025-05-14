variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
}

variable "postgres_password" {
  description = "Password for PostgreSQL database"
  type        = string
  sensitive   = true
}

variable "api_key" {
  description = "API key authentication"
  type        = string
  sensitive   = true
}

variable "database_url" {
  description = "database connection string (SQLAlchemy)"
  type        = string
  sensitive   = true
}

variable "google_client_id" {
  description = "Google OAuth 2.0 frontend login"
  type        = string
}
