#! /bin/bash

docker network create --attachable systemtest_network

docker volume create systemtest_postgres_data
docker volume create systemtest_postgres_data_backups
docker volume create systemtest_traefik_data

docker build -t systemtest_django:beta -f ./compose/production/django/Dockerfile .
docker build -t systemtest_celeryworker:beta -f ./compose/production/django/Dockerfile .
docker build -t systemtest_celerybeat:beta -f ./compose/production/django/Dockerfile .
docker build -t systemtest_flower:beta -f ./compose/production/django/Dockerfile .
docker build -t systemtest_postgres:beta -f ./compose/production/postgres/Dockerfile .
docker build -t systemtest_traefik:beta -f ./compose/production/traefik/Dockerfile .

docker run -d --network systemtest_network --name postgres -v systemtest_postgres_data:/var/lib/postgresql/data:Z -v systemtest_postgres_data_backups:/backups:z --env-file ./.envs/.production/.postgres systemtest_postgres:beta

docker run -d --network systemtest_network --name redis redis:6.0.9

docker run -d --network systemtest_network --name django --env-file ./.envs/.production/.postgres --env-file ./.envs/.production/.django systemtest_django:beta /start

docker run -d --network systemtest_network --name celeryworker --env-file ./.envs/.production/.postgres --env-file ./.envs/.production/.django systemtest_django:beta /start-celeryworker

docker run -d --network systemtest_network --name celerybeat --env-file ./.envs/.production/.postgres --env-file ./.envs/.production/.django systemtest_django:beta /start-celerybeat

docker run -d --network systemtest_network --name flower --env-file ./.envs/.production/.postgres --env-file ./.envs/.production/.django systemtest_django:beta /start-flower

docker run -d --network systemtest_network --name traefik -p 80:80 -p 443:443 -p 5555:5555 -v systemtest_traefik_data:/etc/traefik/acme:z systemtest_traefik:beta
