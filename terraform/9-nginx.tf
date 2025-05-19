/*
  Installs the official NGINX ingress controller via Helm
  The controller gets a LoadBalancer type service, makes sure that GKE creates an external IP en make it publically accessable.
*/

resource "helm_release" "nginx_ingress" {
  name       = "nginx-ingress"
  repository = "https://kubernetes.github.io/ingress-nginx"
  chart      = "ingress-nginx"
  namespace  = "ingress-nginx"

  create_namespace = true

  values = [
    <<EOF
controller:
  service:
    type: LoadBalancer
EOF
  ]
}

/*
  Annotations.Certmanager.io/cluster-issuer = Make sure that cert-manager automatically gets a TLS-cert via Let's encrypt.
*/
resource "kubernetes_ingress_v1" "fastapi_ingress" {
  metadata {
    name = "fastapi-ingress"
    annotations = {
      "cert-manager.io/cluster-issuer"             = "letsencrypt-prod"
    }
  }

  spec {
    ingress_class_name = "nginx"

    tls {
      hosts       = ["tracker.timsmans.be"]
      secret_name = "frontend-tls" # Zelfde TLS cert
    }

    rule {
      host = "tracker.timsmans.be"
      
      http {
        path {
          path      = "/api"
          path_type = "Prefix"

          backend {
            service {
              name = kubernetes_service.fastapi.metadata[0].name
              port {
                number = 80
              }
            }
          }
        }
      }
    }
  }
}


resource "kubernetes_ingress_v1" "frontend_ingress" {
  metadata {
    name      = "frontend-ingress"
    namespace = "default"
    annotations = {
      # Belangrijke aanpassing: gebruik rewrite-target om alle paden naar de root te sturen
      "nginx.ingress.kubernetes.io/rewrite-target" = "/"
      "cert-manager.io/cluster-issuer"             = "letsencrypt-prod"
    }
  }

  spec {
    ingress_class_name = "nginx"

    
    tls {
      hosts       = ["tracker.timsmans.be"] # Domain
      secret_name = "frontend-tls"
    }
    
    rule {
      host = "tracker.timsmans.be"
      http {
        path {
          path      = "/"  
          path_type = "Prefix"
          backend {
            service {
              name = "vue-frontend"
              port {
                number = 80
              }
            }
          }
        }
      }
    }
  }
}
