[![CircleCI](https://circleci.com/gh/marianojabdala/microservices.svg?style=svg)](https://circleci.com/gh/marianojabdala/microservices)

# Flask + Docker + Kubernetes + virtualenv

First attempt to create a micro Architecture that create a user api(CRUD) that
could be deployed using docker-compose and kubernetes(minikube) also runs locally.

### Installation

- Install python virtualenv from: https://github.com/pyenv/pyenv#installation

- Install python 3.x.x with

  pyenv install 3.x.x

* Create a folder where you want to get the code, then clone the application.
  Eg.
  _ mkdir -p /home/[user_name]/tmp/
  _ cd /home/[user_name]/tmp/

* Clone the repository into that folder

* Create a virtualenv with:

  pyenv virtualenv [name].

            Eg. pyenv virtualenv python-3.6

* Activate the virtualenv

       pyenv activate python-3.6

* Install the required modules

       pip install -r requirements.txt

### Usage

There is a Makefile where the nested commands are in place to execute the application

- Run it as production

        make run

- Stop service(This is not the best way, I'll try to improve it)

       make stop

- Run it as development(reload the changes you make on the code.)

        make run-local ( stop with Ctrl+C)

### Testing

There are 3 kind of test: 
1 - Integration test
2 - BDD Tests
3 - Integration tests with postman

#### Details
 1 - Integration test
 To be able to run this test just open the terminal and run
```bash
  make ci
```
this will run also the bdd tests

 2 - BDD Tests
 To be able to run this test just open the terminal and run
```bash
  make bdd
```
 2.1 - bdd-with-reports: This will generate the reports for the bdd test, before run this just read de README.md file inside the bdd folder  

3 - Integration tests with postman
Before run this test the newman package should be installed, to do this npm should be installed in the system.
Then go to the tests/postman folder and type:
```bash
npm install
```
and then go back to the users folder and run this:
```bash
  make ci-with-postam
```

### Using Docker

At the users folder level run:

``bash
       make build_image
```
That command will create the user-service:v1 image

Then run:

       docker-compose -f deploy/docker/docker-compose-*.yml up

For docker-compose-sqlite, run:

    docker-compose -f docker-compose-sqlite.yml up

### Using minikube

- Prequequisites Docker installed

First Install minikube from here: https://github.com/kubernetes/minikube/releases.

Then install kubectl from here:
https://kubernetes.io/docs/tasks/tools/install-kubectl/?#install-kubectl-binary-via-curl

- Initialize minikube

        minikube start

- Run

         eval $(minikube docker-env)

  (This will get into the minikube machine)

- In the same directory as the Dokerfile(users) run the next command:

          docker build -f deploy/docker/Dockerfile --args APP_SETTINGS=development -t user-service:v1 --compress .

After this you are ready to deploy the service and database(postgres) into kubernetes

Run:

    make kub_deploy

For remove the kubernetes deploy run:

    make kub_undeploy

In case the database is not initialized there should be a post to the url with the
/\_init_db endpoint and use the Authentication header with the base64 of BASIC_AUTH_USERNAME:BASIC_AUTH_PASSWORD that is in the .env file

// TODO: Add the docs folder and the files documentation using sphinx.
