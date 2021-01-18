# Online Shop

Andrew's online shop reference guide for deploying a Django, Celery, & Rabbitmq program to kubernetes and Docker.

### Run for development

1. Start up a rabbitmq service (preferably with docker) and expose port 5672

`docker run --rm -it --hostname my-rabbit -p 15672:15672 -p 5672:5672 rabbitmq:3-management`

2. Start up celery:

`celery -A Shop worker --loglevel=info`

3. Start up Django

`python3 manage.py runserver 8080`

### EMAIL settings

The smtp server configured in the Shop/settings.py is for a gmail account. To connect your email to the django server, I recommend creating a new gmail account that must be given "less secure" login permissions in order for django to login to it.

## Run with Docker-Compose

1. Configure Shop/settings.py to point to rabbitmq service labeled 'rabbit':

`CELERY_BROKER_URL = 'amqp://guest:guest@rabbit:5672/'`

2. Configure docker-compose.yaml so the email_username and email_password are set to your less secure gmail account.
3. Configure docker-compose.yml to point to an available port (currently set to port 80)
4. Run the containers:

`docker-compose up --build -d`

## Run with kubernetes

### Pushing docker images

You can optionally push to a local docker repository, otherwise push to docker hub.  To create a local docker repostiory:

`docker run -d -p 0.0.0.0:5000:5000 --restart=always --name registry registry:2`

To push an image to the local repository:

`docker build -t localhost:5000/shop-project:1.0.0 .`

`docker push localhost:5000/shop-project:1.0.0`

### Prepare minikube

1. If you have started minikube before and want to add the insecure-registry, you must delete the previous minikube instanceL

`minikube delete`

2. Start up minikube

`minikube start --driver=hyperv --insecure-registry="{local docker registry IPv4}:5000"`

You can run `ipconfig` and get your wifi or ethernet IPv4 adress for the {local docker registry IPv4}

Parameters:

`--insecure-registry=` this parameter is for accessing a local docker repository, if setup.

`--driver=` this parameter is for choosing a specific VM besides oracle virtualbox.

3. kubectl apply -f kubernetes/ingress.yaml

With the provided ingress yaml, we must expose a host name to connect to the server. Located within the ingress.yaml file, we see the host is currently set to "minikube.local", for this to work on your machine:

a) Enable minikube ingress:

`minikube addons enable ingress`

b) Copy the IP adress for your ingress instance:

`kubectl get ingress minikube-ingress`

c) modify the /etc/hosts file on your computer and add the following:

`{Ingress IP adress} minikube.local`

### Startup Servers

1. configure kubernetes/celery/deployment.yaml and kubernetes/django/deployment.yaml to have the correct env variables for gmail email and password.
1. Apply the rabbitmq deployment:

`kubectl apply -f kubernetes/rabbitmq/`

2. Apply the django server deployment:

`kubectl apply -f kubernetes/django/`

3. Apply the celery deployment:

`kubectl apply -f kubernetes/celery/`

4. Navigate to the minikube.local website and visit /swagger to check that the service is now running
