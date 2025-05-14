resource "kubernetes_secret" "postgres" {
  metadata {
    name = "postgres-secret"
  }

  data = {
    POSTGRES_PASSWORD = var.postgres_password
  }

  type = "Opaque"
}


resource "kubernetes_secret" "fastapi" {
  metadata {
    name = "fastapi-secret"
  }

  data = {
    API_KEY = var.api_key
    DATABASE_URL = var.database_url
  }

  type = "Opaque"
}

resource "kubernetes_secret" "frontend" {
  metadata {
    name = "frontend-secret"
  }

  data = {
    GOOGLE_CLIENT_ID = var.google_client_id
  }

  type = "Opaque"
}