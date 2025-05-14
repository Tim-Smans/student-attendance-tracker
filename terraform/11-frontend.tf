resource "kubernetes_deployment" "frontend" {
  metadata {
    name = "vue-frontend"
    labels = { app = "frontend" }
  }

  spec {
    replicas = 1
    selector {
      match_labels = { app = "frontend" }
    }

    template {
      metadata { labels = { app = "frontend" } }

      spec {
        container {
          name  = "frontend"
          image = "docker.io/timsmans/student-tracking-frontend:latest"
          port { container_port = 80 }
        }
      }
    }
  }
}
