from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from app.models import TenantCreate, DeploymentRequest
from app.services import create_tenant_record, get_tenant, render_deployment

app = FastAPI(
    title="CloudForge Control Plane",
    description="A demo self-service Kubernetes PaaS control-plane API.",
    version="0.1.0",
)

@app.get("/health", tags=["operations"])
def health():
    return {"status": "ok", "service": "cloudforge-control-plane"}

@app.post("/tenants", status_code=201, tags=["tenants"])
def create_tenant(payload: TenantCreate):
    try:
        return create_tenant_record(payload)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc

@app.get("/tenants/{tenant_name}", tags=["tenants"])
def read_tenant(tenant_name: str):
    tenant = get_tenant(tenant_name)
    if tenant is None:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return tenant

@app.post("/deployments", tags=["deployments"])
def create_deployment(payload: DeploymentRequest):
    if get_tenant(payload.tenant) is None:
        raise HTTPException(status_code=404, detail="Create the tenant before deploying")
    return {
        "status": "manifest_generated",
        "tenant": payload.tenant,
        "application": payload.app_name,
        "apply_command": "kubectl apply -f deployment.yaml",
        "manifest": render_deployment(payload),
        "note": "Review generated YAML and cluster policies before applying.",
    }

@app.get("/", response_class=PlainTextResponse, include_in_schema=False)
def root():
    return "CloudForge control plane is running. Visit /docs for the API."
