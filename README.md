# Online Shop

Andrew's online shop

### Run in development

1. Start up a rabbitmq service (preferably with docker)
2. Start up celery:

celery -A Shop worker --loglevel=info

3. Start up Django

python3 manage.py runserver 8080

### Run with Docker-Compose

1. Configure Shop/settings.py to point to rabbitmq service labeled 'rabbit':

CELERY_BROKER_URL = 'amqp://guest:guest@rabbit:5672/'

2. Configure docker-compose.yml to point to an available port (currently set to port 80)
3. Run the command:

docker-compose up --build -d

### Configure .env

The .env file must be located within the inner Shop/ folder

```
SECRET_KEY=fooBar
STRIPE_PUBLISHABLE_KEY=fooBar
STRIPE_SECRET_KEY=fooBar
EMAIL_USERNAME="email"
EMAIL_PASSWORD="password"
EMAIL_RECIPIENTS="email1,email2"
```
