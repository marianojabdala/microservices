SHELL=/bin/bash

export APP_NAME=microservices

export TMP_DIR=$(shell mktemp -d)

MAKEFLAGS += --no-print-directory

BDD_BASE_PATH=$(PWD)/tests/bdd

ALLURE_OUTPUT_PATH=allure.output

ALLURE_REPORT_PATH=$(BDD_BASE_PATH)/allure-report

run:
	PYTHONPATH=../ DAEMON=true APP_SETTINGS=production gunicorn --config config.py app:APP

run-local:
	make lint
	PYTHONPATH=../ APP_SETTINGS=development gunicorn --reload --config config.py app:APP

stop:
	@echo ******Shutting down server******
	pkill gunicorn

lint:

	pylint --rcfile=pylintrc --ignore=config.py,tests,setup.py,models,dtos,swagger,test_app.py users

bdd:
	PYTHONPATH=../  behave -x

bdd-with-reports:
	make bdd
	allure generate --clean $(ALLURE_OUTPUT_PATH) -o $(ALLURE_REPORT_PATH)
	cp $(BDD_BASE_PATH)/categories.json $(ALLURE_REPORT_PATH)
	allure open $(ALLURE_REPORT_PATH)

bdd:
	behave

ci:

	make lint
	TEST_DATABASE_NAME='microservices' TEST_DATABASE_PATH=$(shell echo $(TMP_DIR))/tests-microservices.sqlite python -m pytest tests/integration -v --cov=users --html=test_reports/report-$(shell  date +%Y-%m-%d).html
	make bdd
	make ci-with-postman

	@echo ******Cleaning up******
	make cleanup

ci-with-postman:
	@echo ******Raising new app for testing******

	PYTHONPATH="../" TEST_DATABASE_NAME='microservices' TEST_DATABASE_PATH=$(shell echo $(TMP_DIR))/tests-microservices.sqlite nohup gunicorn --config tests/config.py test_app:APP&
	@echo ******Waiting for app to be ready...******
	sleep 10
	@echo ******Running Postman tests******
	tests/node_modules/.bin/newman run --verbose tests/postman/Users.postman_collection.json -e tests/postman/Microservices.postman_environment.json
	@echo ******Running python integration tests******
	pkill gunicorn

build_image:
	docker build -f deploy/docker/Dockerfile --build-arg APP_SETTINGS=development -t user-service:v1 --compress .

cleanup:
	@echo ******Shutting down server******
	rm -rf /tmp/tmp.*


clean:
	@find . -name "__pycache__" | xargs rm -fr

docs:
	PYTHONPATH="../" sphinx-apidoc -M -o ../docs/source . tests test_app.py; cd ../docs; PYTHONPATH="../users" make html

build_image:
	docker build -f deploy/docker/Dockerfile --build-arg APP_SETTINGS=development -t user-service:v1 --compress .


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
