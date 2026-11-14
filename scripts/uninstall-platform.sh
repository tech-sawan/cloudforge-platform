#!/usr/bin/env bash
set -euo pipefail

# This removes Helm releases, not CRDs or persistent data that may have been
# created separately. Review the target cluster before running.
helm uninstall cloudforge -n argocd || true
helm uninstall cloudforge-monitoring -n monitoring || true
helm uninstall cert-manager -n cert-manager || true
helm uninstall traefik -n traefik || true
helm uninstall external-secrets -n external-secrets || true

echo "Helm releases removed. Review and clean up namespaces/CRDs separately."
