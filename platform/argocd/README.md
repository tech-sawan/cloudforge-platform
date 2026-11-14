# Argo CD application example

This is an example of Argo CD managing an upstream Helm chart declaratively.
Replace `https://github.com/YOUR_ORG/YOUR_REPO.git` with the Git repository that
contains your configuration. `targetRevision` is intentionally a placeholder:
pin a real chart version before applying.

Apply only after Argo CD is installed:

```bash
kubectl apply -f platform/argocd/sample-app.yaml
```
