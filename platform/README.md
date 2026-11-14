# Open-source platform components

CloudForge deliberately composes proven open-source projects instead of rebuilding
ingress, GitOps, certificate management, or observability itself.

The install script installs upstream/community Helm charts and keeps only CloudForge-
specific overrides in this repository.

| Component | Purpose | Helm chart |
|---|---|---|
| Traefik | HTTP routing and Kubernetes Gateway API support | `traefik/traefik` |
| cert-manager | TLS certificate lifecycle | `jetstack/cert-manager` |
| kube-prometheus-stack | Prometheus, Alertmanager, Grafana, exporters and Prometheus Operator | `prometheus-community/kube-prometheus-stack` |
| Argo CD | GitOps continuous delivery | `argo/argo-cd` |
| External Secrets Operator | Sync secrets from an external secrets manager | `external-secrets/external-secrets` (optional) |

## Install

From the repository root, after creating the Kind cluster:

```bash
./scripts/install-platform.sh
```

To include External Secrets Operator:

```bash
INSTALL_EXTERNAL_SECRETS=true ./scripts/install-platform.sh
```

The script uses upstream Helm repositories and the values files in `platform/helm-values`.
For repeatable production deployments, pin and review chart versions in your release
process, scan images, review chart permissions, and promote the same versions through
development/staging/production.

## Local access

```bash
# Grafana (local demo credentials are defined in values; change them)
kubectl -n monitoring port-forward svc/cloudforge-monitoring-grafana 3000:80

# Argo CD API/UI
kubectl -n argocd port-forward svc/cloudforge-argocd-server 8080:80
```

Traefik HTTP entrypoint: http://127.0.0.1:8081  
Grafana: http://127.0.0.1:3000  
Argo CD: http://127.0.0.1:8080

Get the initial Argo CD admin password:

```bash
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath='{.data.password}' | base64 -d; echo
```

The Grafana demo password is `change-me-local-only` in this local Kind profile.
Do not use these demo credentials in a shared or production environment.

## Traefik and Gateway API

The project uses Traefik rather than Traefik. Kubernetes retired Traefik
in March 2026, so new deployments should use a maintained controller and plan around
Gateway API. CloudForge installs the Gateway API Standard CRDs and enables Traefik's
Gateway API provider. For local access:

```bash
kubectl -n traefik port-forward svc/traefik 8081:80
```

The port-forward is sufficient for local exploration; add Gateway and HTTPRoute
resources for application routing. See the [Traefik Kubernetes guide](https://doc.traefik.io/traefik/getting-started/kubernetes/).

## cert-manager

The chart installs cert-manager and its CRDs. A ClusterIssuer is intentionally not
created automatically: a real ACME issuer needs a domain you control, working public
DNS, reachable challenge endpoints, and a valid email address. See
`cert-manager` documentation before creating a production issuer.

## GitOps bootstrap

`argocd/` contains an example Application that demonstrates Argo CD managing a
Helm chart from its upstream repository. Replace the sample Git URL and pin the
chart version before using it for a real environment.

## Notes

- `kube-prometheus-stack` includes Grafana and commonly includes kube-state-metrics
  and node-exporter dependencies. Avoid installing duplicate copies separately.
- Helm values are configuration overlays, not forks of upstream charts.
- External Secrets Operator is optional because it needs a configured SecretStore
  or ClusterSecretStore and credentials for a provider such as AWS Secrets Manager,
  Azure Key Vault, or HashiCorp Vault.
- The default values are for local demonstration, not high availability or production.
