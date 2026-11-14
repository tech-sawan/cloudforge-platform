# 5-minute client demo

1. Start the API and open `/docs`.
2. Create a tenant called `acme`.
3. Deploy `nginx:1.27` with two replicas through the API.
4. Explain how the generated YAML creates a namespace, Deployment and Service.
5. Apply the manifest to a local Kind cluster and inspect:
   `kubectl get all -n tenant-acme`
6. Show the GitHub Actions checks and discuss how the same workflow extends to EKS,
   AKS or OKE using Terraform and Helm.

Talk track: "CloudForge turns a developer's deployment request into a governed,
repeatable Kubernetes deployment. The control plane is the product; Kubernetes is
the execution layer."
