from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_tenant_and_deployment_manifest():
    tenant = client.post("/tenants", json={
        "name": "demo-team", "display_name": "Demo Team"
    })
    assert tenant.status_code == 201
    assert tenant.json()["namespace"] == "tenant-demo-team"

    deployment = client.post("/deployments", json={
        "tenant": "demo-team",
        "app_name": "sample-api",
        "image": "nginx:1.27",
        "port": 80,
        "replicas": 2
    })
    assert deployment.status_code == 200
    body = deployment.json()
    assert body["status"] == "manifest_generated"
    assert "kind: Deployment" in body["manifest"]
    assert "kind: Service" in body["manifest"]

def test_reject_invalid_tenant_name():
    response = client.post("/tenants", json={
        "name": "Bad_Name", "display_name": "Bad Name"
    })
    assert response.status_code == 422
