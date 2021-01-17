# Online Shop

Andrew's online shop

### Run in development

1. Start up a rabbitmq service (preferably with docker) and expose port 5672

docker run --rm -it --hostname my-rabbit -p 15672:15672 -p 5672:5672 rabbitmq:3-management

2. Start up celery:

celery -A Shop worker --loglevel=info

3. Start up Django

python3 manage.py runserver 8080

### Run with Docker-Compose

1. Configure Shop/settings.py to point to rabbitmq service labeled 'rabbit':

CELERY_BROKER_URL = 'amqp://guest:guest@rabbit:5672/'

2. Configure docker-compose.yml to point to an available port (currently set to port 80)
3. Run the containers:

docker-compose up --build -d

### EMAIL settings

The smtp server configured in the Shop/settings.py is for a gmail account. To connect your email to the django server, I recommend creating a new gmail account that must be given "less secure" login permissions in order for django to login to it.

### Configure Shop/local_settings.py

```
SECRET_KEY=fooBar
STRIPE_PUBLISHABLE_KEY=fooBar
STRIPE_SECRET_KEY=fooBar
EMAIL_HOST_USER="email"
EMAIL_HOST_PASSWORD="password"
```

the STRIPE keys are currently not being used and can be set to "fooBar"

### Pushing docker images

Since the image contains credentials (local_settings), create your own local registry to push the images to, instead of the public docker hub repository:

docker run -d -p 5000:5000 --restart=always --name registry registry:2

To push an image:

docker build -t localhost:5000/shop-project:1.0.0 .

docker push localhost:5000/shop-project:1.0.0
