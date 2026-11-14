import re
from pydantic import BaseModel, Field, field_validator

DNS_LABEL = re.compile(r"^[a-z0-9]([-a-z0-9]*[a-z0-9])?$")

def validate_dns_label(value: str) -> str:
    if len(value) > 63 or not DNS_LABEL.fullmatch(value):
        raise ValueError("must be a lowercase Kubernetes DNS label (max 63 characters)")
    return value

class TenantCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=40)
    display_name: str = Field(..., min_length=2, max_length=80)

    @field_validator("name")
    @classmethod
    def valid_name(cls, value):
        return validate_dns_label(value)

class DeploymentRequest(BaseModel):
    tenant: str
    app_name: str
    image: str = Field(..., min_length=3, max_length=200)
    port: int = Field(default=8080, ge=1, le=65535)
    replicas: int = Field(default=2, ge=1, le=10)
    cpu_request: str = "100m"
    memory_request: str = "128Mi"
    cpu_limit: str = "500m"
    memory_limit: str = "256Mi"

    @field_validator("tenant", "app_name")
    @classmethod
    def valid_dns_names(cls, value):
        return validate_dns_label(value)

    @field_validator("image")
    @classmethod
    def safe_image_reference(cls, value):
        if any(ch.isspace() for ch in value) or value.startswith("-"):
            raise ValueError("invalid container image reference")
        return value
