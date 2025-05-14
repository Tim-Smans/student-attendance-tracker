resource "kubernetes_deployment" "fastapi" {
  metadata {
    name = "fastapi"
    labels = { app = "fastapi" }
  }

  spec {
    replicas = 2
    selector {
      match_labels = { app = "fastapi" }
    }

    template {
      metadata { labels = { app = "fastapi" } }

      spec {
        container {
          name  = "fastapi"
          image = "docker.io/timsmans/student-tracking-api:latest"
          port { container_port = 80 }

          env {
            name = "API_KEY"
            value_from {
              secret_key_ref {
                name = "fastapi-secret"
                key  = "API_KEY"
              }
            }
          }
          env {
            name = "DATABASE_URL"
            value_from {
              secret_key_ref {
                name = "fastapi-secret"
                key  = "DATABASE_URL"
              }
            }
          }
        }
      }
    }
  }
}


resource "kubernetes_service" "fastapi" {
  metadata {
    name = "fastapi"
    labels = { app = "fastapi" }
  }
  spec {
    type = "ClusterIP"

    selector = {
      app = "fastapi"
    }

    port {
      protocol = "TCP"
      port     = 80
      target_port = 80
    }
  }
}
