export APP_NAME=microservices

TEST_DATABASE_NAME=tests/tests-microservices.sqlite

MAKEFLAGS += --no-print-directory

SHELL=/bin/bash

run:
	DAEMON=true APP_SETTINGS=production gunicorn --config config.py app:app

run-local:
	APP_SETTINGS=development gunicorn --reload --config config.py app:app

stop:
	@echo ******Shutting down server******
	pkill gunicorn

ci:
	PYTHONPATH="../" DAEMON=true gunicorn --config tests/config.py test_app:app
	@echo ******Waiting for app to be ready...******
	sleep 5
	@echo ******Running Postman tests******
	newman run tests/postman/Users.postman_collection.json -e tests/postman/Microservices.postman_environment.json
	@echo ******Running python integration tests******
	PYTHONPATH="../" python -m pytest tests/integration -v
	@echo ******Raising new app for testing******
	make cleanup

cleanup:
	@echo ******Shutting down server******
	pkill gunicorn
	rm $(TEST_DATABASE_NAME)

docs:
	sphinx-apidoc -f -o ../docs/source .; cd ..; make html

kube_setup:
	 @echo "Be sure you run #eval (minikube docker-env) before kube_deploy or kube_undeploy"

kube_deploy:
	make kube_setup
	kubectl create secret generic postgres-pass --from-literal=password=mysecretpassword
	kubectl create -f deploy/kubernetes/db-claim-persistentvolumeclaim.yaml
	kubectl create -f deploy/kubernetes/db-deployment.yaml
	kubectl create -f deploy/kubernetes/db-service.yaml
	kubectl create -f deploy/kubernetes/users-deployment.yaml
	kubectl create -f deploy/kubernetes/users-service.yaml
	kubectl create -f deploy/kubernetes/users-hpa.yaml
	minikube service users

kube_undeploy:
	make kube_setup
	kubectl delete deployment -l app=users
	kubectl delete service -l app=users
	kubectl delete pvc -l app=users
	kubectl delete hpa -l app=users
	kubectl delete secret postgres-pass


.PHONY:run ci run-local kube_deploy kube_undeploy docs
