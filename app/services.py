from app.models import TenantCreate, DeploymentRequest

# Demo-only in-memory store. Replace with PostgreSQL for a real service.
_TENANTS: dict[str, dict] = {}

def create_tenant_record(payload: TenantCreate) -> dict:
    if payload.name in _TENANTS:
        raise ValueError("Tenant already exists")
    record = {
        "name": payload.name,
        "display_name": payload.display_name,
        "namespace": f"tenant-{payload.name}",
        "status": "active",
    }
    _TENANTS[payload.name] = record
    return record

def get_tenant(name: str):
    return _TENANTS.get(name)

def render_deployment(payload: DeploymentRequest) -> str:
    namespace = f"tenant-{payload.tenant}"
    app = payload.app_name
    # All interpolated names are validated DNS labels; resource quantities are
    # constrained to a conservative Kubernetes quantity pattern below.
    for quantity in (payload.cpu_request, payload.cpu_limit,
                     payload.memory_request, payload.memory_limit):
        if not quantity or len(quantity) > 16 or not all(c.isalnum() or c in ".-" for c in quantity):
            raise ValueError("Invalid Kubernetes resource quantity")
    return f'''apiVersion: v1
kind: Namespace
metadata:
  name: {namespace}
  labels:
    app.kubernetes.io/managed-by: cloudforge
    cloudforge.io/tenant: {payload.tenant}
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {app}
  namespace: {namespace}
  labels:
    app.kubernetes.io/name: {app}
spec:
  replicas: {payload.replicas}
  selector:
    matchLabels:
      app.kubernetes.io/name: {app}
  template:
    metadata:
      labels:
        app.kubernetes.io/name: {app}
    spec:
      containers:
        - name: {app}
          image: {payload.image}
          ports:
            - name: http
              containerPort: {payload.port}
          resources:
            requests:
              cpu: "{payload.cpu_request}"
              memory: "{payload.memory_request}"
            limits:
              cpu: "{payload.cpu_limit}"
              memory: "{payload.memory_limit}"
          readinessProbe:
            tcpSocket:
              port: http
            initialDelaySeconds: 5
            periodSeconds: 10
          livenessProbe:
            tcpSocket:
              port: http
            initialDelaySeconds: 15
            periodSeconds: 20
---
apiVersion: v1
kind: Service
metadata:
  name: {app}
  namespace: {namespace}
spec:
  type: ClusterIP
  selector:
    app.kubernetes.io/name: {app}
  ports:
    - name: http
      port: 80
      targetPort: http
'''
