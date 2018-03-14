#Flask + Docker + Kubernetes + virtualenv

First attempt to create a micro Architecture that create a user api(CRUD) that
could be deployed using docker-compose and kubernetes(minikube) also runs locally.

###Installation

 - Install python virtualenv from: https://github.com/pyenv/pyenv#installation

 - Install python 3.6.x with 

    pyenv install 3.6.x

        
 - Create a folder where you want to get the code, then clone the application.
Eg. 
    * mkdir -p /home/[user_name]/tmp/
    * cd /home/[user_name]/tmp/ 

 - Clone the repository into that folder

- Create a virtualenv with:
 
    pyenv virtualenv [name].
            
            Eg. pyenv virtualenv python-3.6
 - Activate the virtualenv 
 
        pyenv activate python-3.6

 - Install the required modules
 
        pip install -r requirements.txt

###Usage
There is a Makefile where the nested commands are in place to execute the application

- Run it as production
    
        make run
- Stop service(This is not the best way, I'll try to improve it)
    
       make stop
     
- Run it as development(reload the changes you make on the code.)
    
        make run-local ( stop with Ctrl+C)

###Using Docker

### Using minikube
 - Prequequisites Docker installed
 
 
First Install minikube from here: https://github.com/kubernetes/minikube/releases.

Then install kubectl from here:
https://kubernetes.io/docs/tasks/tools/install-kubectl/?#install-kubectl-binary-via-curl
  
* Initialize minikube 
        
        minikube start

* Run  
    
        eval $(minikube docker-env)
 (This wiil get into the minikube machine)
 
* In the same directory as the Dokerfile(users) run the next command:
 
          docker build -t user-service:v1 --compress .
 
After this you are ready to deploy the service and database(postgres) into kuberntes

Go to the folder users/deploy 



   Basic YWRtaW46XHg4Yl1ePlx4ODFceDgxXHg5ZFx4OGRceGM3Mw==
