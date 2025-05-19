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
          image = "docker.io/timsmans/student-tracking-frontend:v11-download-page"
          image_pull_policy = "Always"
          port { container_port = 80 }
        }
      }
    }
  }
}



resource "kubernetes_service" "frontend" {
  metadata {
    name = "vue-frontend"
    labels = { app = "frontend" }
  }
  spec {
    type = "ClusterIP"

    selector = {
      app = "frontend"
    }

    port {
      protocol = "TCP"
      port     = 80
      target_port = 80
    }
  }
}
