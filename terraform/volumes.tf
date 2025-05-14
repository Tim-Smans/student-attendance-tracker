resource "kubernetes_persistent_volume_claim" "postgres" {
  metadata {
    name = "postgres-pvc"
  }

  spec{
    access_modes = ["ReadWriteOnce"]

    resources {
      requests = {
        storage = "25Gi"
      }
    }

    storage_class_name = "standard"
  }
}