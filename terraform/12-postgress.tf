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
          port {
            container_port = 5432
          }
        }
      }
    }
  }
}
