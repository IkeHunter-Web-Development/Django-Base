# Celery Setup

1. Add pip packages:

   ```txt
   # Celery
   celery>=5.4.0,<5.5
   redis>=5.0.4,<5.1
   django-celery-beat>=2.7.0,<2.8
   ```

2. Add `app/app/celery.py`:

   ```py
   import os
   from celery import Celery

   os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

   app = Celery("app")

   app.config_from_object("django.conf:settings", namespace="CELERY")

   app.autodiscover_tasks()
   ```

3. Add the following to `settings.py`:

   ```python
   INSTALLED_APPS = [
    "django_celery_beat",
    ...
   ]

   # Celery Configuration
   CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")
   CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND")
   CELERY_TASK_ACKS_LATE = bool(int(os.environ.get("CELERY_TASK_ACKS_LATE", "1")))
   CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = bool(
       int(os.environ.get("CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP", "1"))
   )
   CELERY_ACCEPT_CONTENT = ["json"]
   CELERY_TASK_SERIALIZER = "json"
   CELERY_RESULT_SERIALIZER = "json"
   CELERY_TIMEZONE = "UTC"
   CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

   # Custom schedules
   CELERY_BEAT_SCHEDULE = {}
   ```

4. Add the following to `app/app/__init__.py`:

   ```python
   from .celery import app as celery_app

   __all__ = ("celery_app",)
   ```

5. Add Celery containers to docker compose:

   ```yml
   app:
     # ...
     environment:
        # ...
        - CELERY_BROKER_URL=redis://__NAME__-dev-redis:6379/0
        - CELERY_RESULT_BACKEND=redis://__NAME__-dev-redis:6379/0
        - CELERY_ACKS_LATE=True
        - DJANGO_DB=postgresql
        - DJANGO_REDIS_URL=redis://__NAME__-dev-redis:6379/1
    depends_on:
        # ...
        - redis

   redis:
     image: redis:alpine
     container_name: __NAME__-dev-redis
     ports:
       - 6379:6379

   celery:
     build:
       context: .
       args:
         - DEV=true
     restart: unless-stopped
     user: django-user
     command: ['celery', '-A', 'app', 'worker', '--loglevel=info']
     volumes:
       - ./app:/app
       - static-__NAME__-dev:/vol/web
     depends_on:
       - redis
       - postgres
     environment:
       - DEBUG=1
       - CELERY_BROKER_URL=redis://__NAME__-dev-redis:6379/0
       - CELERY_RESULT_BACKEND=redis://__NAME__-dev-redis:6379/0
       - DJANGO_DB=postgresql

       - POSTGRES_HOST=__NAME__-dev-db
       - POSTGRES_PORT=5432
       - POSTGRES_NAME=devdatabase
       - POSTGRES_DB=devdatabase
       - POSTGRES_USER=devuser
       - POSTGRES_PASSWORD=devpass

   celerybeat:
     build:
       context: .
       args:
         - DEV=true
     user: django-user
     restart: unless-stopped
     command:
       [
         'celery',
         '-A',
         'app',
         'beat',
         '--loglevel=info',
         '--scheduler',
         'django_celery_beat.schedulers:DatabaseScheduler'
       ]
     volumes:
       - ./app:/app
       - static-__NAME__-dev:/vol/web
     depends_on:
       - redis
       - db
       - celery
     environment:
       - DEBUG=1
       - CELERY_BROKER_URL=redis://__NAME__-dev-redis:6379/0
       - CELERY_RESULT_BACKEND=redis://__NAME__-dev-redis:6379/0
       - DJANGO_DB=postgresql

       - POSTGRES_HOST=__NAME__-dev-db
       - POSTGRES_PORT=5432
       - POSTGRES_NAME=devdatabase
       - POSTGRES_USER=devuser
       - POSTGRES_PASSWORD=devpass
       
       - DB_HOST=__NAME__-dev-db
       - DB_NAME=devdatabase
       - DB_USER=devuser
       - DB_PASS=devpass
   ```

6. Add the above config to the network docker compose file, replace `dev` with `network` where necessary.

## Resources

- <https://medium.com/django-unleashed/asynchronous-tasks-in-django-a-step-by-step-guide-to-celery-and-docker-integration-b6f9898b66b5>
- <https://realpython.com/asynchronous-tasks-with-django-and-celery/>
- <https://saasitive.com/tutorial/django-celery-redis-postgres-docker-compose/>
