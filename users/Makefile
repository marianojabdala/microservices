export APP_NAME=microservices

export TMP_DIR=$(shell mktemp -d)

export TEST_DATABASE_NAME=$(shell echo $(TMP_DIR))/tests-microservices.sqlite

MAKEFLAGS += --no-print-directory

SHELL=/bin/bash

BDD_BASE_PATH=$(PWD)/tests/bdd

ALLURE_OUTPUT_PATH=allure.output

ALLURE_REPORT_PATH=$(BDD_BASE_PATH)/allure-report

run:
	DAEMON=true APP_SETTINGS=production gunicorn --config config.py app:APP

run-local:
	APP_SETTINGS=development gunicorn --reload --config config.py app:APP

stop:
	@echo ******Shutting down server******
	pkill gunicorn

lint:
	pylint --ignore=config.py users tests

bdd:
	behave
	allure generate --clean $(ALLURE_OUTPUT_PATH) -o $(ALLURE_REPORT_PATH)
	cp $(BDD_BASE_PATH)/categories.json $(ALLURE_REPORT_PATH)
	allure open $(ALLURE_REPORT_PATH)

ci:
	make lint
	PYTHONPATH="../" python -m pytest tests/integration -v
	@echo ******Cleaning up******
	make cleanup

ci-with-postman:
	make ci
	@echo ******Raising new app for testing******
	PYTHONPATH="../" DAEMON=true gunicorn --config tests/config.py test_app:APP
	@echo ******Waiting for app to be ready...******
	sleep 5
	@echo ******Running Postman tests******
	newman run tests/postman/Users.postman_collection.json -e tests/postman/Microservices.postman_environment.json
	@echo ******Running python integration tests******
	pkill gunicorn

cleanup:
	@echo ******Shutting down server******
	rm -rf /tmp/tmp.*

clean:
	@find . -name "__pycache__" | xargs rm -fr

docs:
	PYTHONPATH="../" sphinx-apidoc -M -o ../docs/source . tests test_app.py; cd ../docs; PYTHONPATH="../users" make html

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


.PHONY:run ci run-local kube_deploy kube_undeploy docs lint
.SILENT: bdd
