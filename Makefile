.PHONY: install run test lint docker-build kind-up kind-down
install:
	python3 -m pip install -r requirements-dev.txt
run:
	uvicorn app.main:app --reload
test:
	pytest -q
lint:
	ruff check app tests
docker-build:
	docker build -t cloudforge-control-plane:0.1.0 .
kind-up:
	kind create cluster --config infra/kind/kind-config.yaml --name cloudforge
kind-down:
	kind delete cluster --name cloudforge
