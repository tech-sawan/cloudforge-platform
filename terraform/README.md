# Terraform infrastructure starter

This folder is the extension point for cloud-specific infrastructure. Keep provider
credentials out of the repository and use remote state with locking for team use.

Suggested implementation:
- AWS: VPC, private subnets, EKS, managed node groups, ECR, IAM roles for service accounts.
- Azure: VNet, AKS, ACR, managed identities, Log Analytics.
- OCI: VCN, OKE, OCIR, IAM policies and OCI Monitoring.

Add a provider-specific root module and pin provider versions before using it. Review
plans and apply only in an isolated development account. No cloud resources are created
by this starter.
