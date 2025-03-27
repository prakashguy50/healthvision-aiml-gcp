.PHONY: init build test deploy clean

init:
	terraform -chdir=config/terraform init
	gcloud config set project $$(gcloud config get-value project)

build:
	mvn clean package -DskipTests
	docker-compose -f config/docker/docker-compose.yml build

test:
	mvn test
	python -m pytest ml-pipeline/model_training/tests/

deploy:
	terraform -chdir=config/terraform apply -auto-approve
	kubectl apply -f config/k8s/

monitor:
	watch kubectl get pods,svc,ing

clean:
	mvn clean
	docker system prune -f