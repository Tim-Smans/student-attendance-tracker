resource "kubernetes_deployment" "fastapi" {
  metadata {
    name = "fastapi-backend"
    labels = {
      app = "fastapi"
    }
  }

  spec {
    replicas = 2
    selector {
      match_labels = {
        app = "fastapi"
      }
    }
    template {
      metadata {
        labels = {
          app = "fastapi"
        }
      }
      spec {
        container {
          name  = "fastapi"
          image = "gcr.io/${var.project_id}/fastapi-backend:latest"
          port {
            container_port = 80
          }
        }
      }
    }
  }
}


resource "kubernetes_secret" "postgres" {
  metadata {
    name = "postgres-secret"
  }

  data = {
    POSTGRES_PASSWORD = base64encode(var.postgres_password)
  }

  type = "Opaque"
}

resource "kubernetes_deployment" "postgres" {
  metadata {
    name = "postgres-db"
    labels = {
      app = "postgres"
    }
  }

  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "postgres"
      }
    }

    template {
      metadata {
        labels = {
          app = "postgres"
        }
      }

      spec {
        container {
          name  = "postgres"
          image = "postgres:14"
          env {
            name  = "POSTGRES_PASSWORD"
            value_from {
                secret_key_ref {
                  name = kubernetes_secret.postgres.metadata[0].name
                  key  = "POSTGRES_PASSWORD"
                }
            }     
          }
          ports {
            container_port = 5432
          }
        }
      }
    }
  }
}


resource "kubernetes_service" "fastapi" {
  metadata {
    name = "fastapi-service"
  }

  spec {
    selector = {
      app = "fastapi"
    }
    port {
      port        = 80
      target_port = 80
    }
    type = "LoadBalancer"
  }
}