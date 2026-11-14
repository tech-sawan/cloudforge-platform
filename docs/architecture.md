# Architecture and design decisions

## Control plane responsibilities
- Accept declarative deployment intent over an API.
- Validate tenant, application, image and resource configuration.
- Produce a Kubernetes workload specification.
- Expose health endpoints for orchestration and monitoring.

## Current demo boundaries
The initial version stores tenant metadata in process memory and returns YAML rather
than applying it to a cluster. This keeps the demo safe and easy to run locally.

## Production evolution
1. Replace in-memory metadata with PostgreSQL and migrations.
2. Add a Kubernetes client and asynchronous reconciliation worker.
3. Add OIDC, tenant authorization and audit events.
4. Add per-tenant quotas, network policies and admission controls.
5. Add ingress, TLS, registry integration and secret management.
6. Add deployment history, status watch, rollback and drift detection.
