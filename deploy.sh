#! /bin/bash
podman pod create --name systemtest -p 80:5000 -p 5555:5555

podman volume create systemtest_postgres_data
podman volume create systemtest_postgres_data_backups

podman build -t systemtest_postgres:beta -f ./compose/production/postgres/Dockerfile .
podman build -t systemtest_django:beta -f ./compose/production/django/Dockerfile .
podman build -t systemtest_celeryworker:beta -f ./compose/production/django/Dockerfile .
podman build -t systemtest_celerybeat:beta -f ./compose/production/django/Dockerfile .
podman build -t systemtest_flower:beta -f ./compose/production/django/Dockerfile .

podman run -d --pod systemtest --name postgres -v systemtest_postgres_data:/var/lib/postgresql/data:Z -v systemtest_postgres_data_backups:/backups:z --env-file ./.envs/.production/.postgres systemtest_postgres:beta

podman run -d --pod systemtest --name redis redis:6.0.9

podman run -d --pod systemtest --name django --env-file ./.envs/.production/.postgres --env-file ./.envs/.production/.django systemtest_django:beta /start

podman run -d --pod systemtest --name celeryworker --env-file ./.envs/.production/.postgres --env-file ./.envs/.production/.django systemtest_django:beta /start-celeryworker

podman run -d --pod systemtest --name celerybeat --env-file ./.envs/.production/.postgres --env-file ./.envs/.production/.django systemtest_django:beta /start-celerybeat

podman run -d --pod systemtest --name flower --env-file ./.envs/.production/.postgres --env-file ./.envs/.production/.django systemtest_django:beta /start-flower

podman run -d --pod systemtest --name nginx -v ./compose/production/nginx/nginx.conf:/ect/nginx/conf.d/default.conf nginx:1.19
