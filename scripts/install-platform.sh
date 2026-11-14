#!/usr/bin/env bash
set -euo pipefail

command -v helm >/dev/null || { echo "helm is required"; exit 1; }
command -v kubectl >/dev/null || { echo "kubectl is required"; exit 1; }

helm repo add traefik https://traefik.github.io/charts
helm repo add jetstack https://charts.jetstack.io
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add argo https://argoproj.github.io/argo-helm
helm repo add external-secrets https://charts.external-secrets.io
helm repo update

# Gateway API CRDs are maintained separately from the Traefik chart.
kubectl apply -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.6.3/standard-install.yaml

helm upgrade --install traefik traefik/traefik \
  --namespace traefik --create-namespace \
  --values platform/helm-values/traefik.yaml \
  --wait --timeout 10m

helm upgrade --install cert-manager jetstack/cert-manager \
  --namespace cert-manager --create-namespace \
  --values platform/helm-values/cert-manager.yaml \
  --wait --timeout 10m

helm upgrade --install cloudforge-monitoring \
  prometheus-community/kube-prometheus-stack \
  --namespace monitoring --create-namespace \
  --values platform/helm-values/kube-prometheus-stack.yaml \
  --wait --timeout 15m

helm upgrade --install cloudforge argo/argo-cd \
  --namespace argocd --create-namespace \
  --values platform/helm-values/argo-cd.yaml \
  --wait --timeout 15m

if [[ "${INSTALL_EXTERNAL_SECRETS:-false}" == "true" ]]; then
  helm upgrade --install external-secrets external-secrets/external-secrets \
    --namespace external-secrets --create-namespace \
    --values platform/helm-values/external-secrets.yaml \
    --wait --timeout 10m
fi

echo
echo "CloudForge platform components installed."
echo "Traefik: kubectl -n traefik port-forward svc/traefik 8081:80"
echo "Grafana: kubectl -n monitoring port-forward svc/cloudforge-monitoring-grafana 3000:80"
echo "Argo CD: kubectl -n argocd port-forward svc/cloudforge-argocd-server 8080:80"
echo "External Secrets Operator is installed only when INSTALL_EXTERNAL_SECRETS=true."
