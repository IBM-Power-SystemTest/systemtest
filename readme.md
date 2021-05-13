<img src="./systemtest/static/images/logos/rebus_h_black.png" alt="IBM rebus Logo" title="IBM" align="right" height="55">

# PowerTest WebApps

![python] ![django-logo] ![celery-logo]

![postgres] ![redis-logo]

![docker-logo] ![podman-logo]

<details>
<summary>Index</summary>

## Content table

- [Requirements](#Requirements)
  - [Dependencies](#Dependencies)
  - [Envs](#Envs)
    - [Local](#Envs---Local)
    - [Production](#Envs---Local)
- [Run](#Run)
  - [Local](#Run---Local)
  - [Production](#Run---Production)
- [Update](#Update)
  - [Local](#Update---Local)
  - [Production](#Update---Production)
- [Links](#![links]-Links-&-References)
- [License](#![license]-License)
- [Author](#![author]-Author)

</details>

Django Web Applications for PowerTest

<br/>

## Requirements

> podman >= 2.2.1 </br>
> podman-composer >= 0.1.7dev

> docker >= 20.10.6 </br>
> docker-compose >= 1.29.1

</br>

> Python >= 3.9 <br/>
> Pip >= 21 <br/>
> PostgreSQL >=13 <br/>
> Redis >= 6

### Dependencies

<details>
<summary> Modules </summary>

> [pytz==2020.4][pytz] <br/>
> [python-slugify==4.0.1][python-slugify] <br/>
> [Pillow==8.0.1][pillow] <br/>
> [argon2-cffi==20.1.0][argon2] <br/>
> [whitenoise==5.2.0][whitenoise] <br/>
> [redis==3.5.3][redis-py] <br/>
> [hiredis==1.1.0][hiredis] <br/>
> [uvicorn[standard]==0.13.1][uvicorn] <br/>
> [ibm-db==3.0.3][ibmdb] <br/>
> [psycopg2==2.8.6][psycopg2] <br/>
> <br>
> [celery==4.4.7][celery] <br/>
> [django-celery-beat==2.1.0][celery-beat] <br/>
> [django-timezone-field==4.1.1][celery-timezone] <br/>
> [flower==0.9.5][flower] <br/>
> <br>
> [django==3.1.5][django] <br/>
> [django-environ==0.4.5][environ] <br/>
> [django-redis==4.12.1][django-redis] <br/>

<br/>

### Dependecies - Local

> [Werkzeug==1.0.1][werkzeug] <br/>
> [ipdb==0.13.4][ipdb] <br/>
> [watchgod==0.6][watchdog] <br/>
> <br/>
> [pylint-django==2.3.0][pylint-django] <br/>
> [pylint-celery==0.3][pylint-celery] <br/>
> <br/>
> [django-debug-toolbar==3.2][toolbar] <br/>
> [django-extensions==3.1.0][django-extensions] <br/>

<br/>

### Dependecies - Production

> gunicorn==20.0.4

</details><br/>

### Envs

### Envs - Local

<details>
<summary> envs </summary>

Envs for _Django_ - **./.envs/.django.local.env**

```bash
# General
# ------------------------------------------------------------------------------
USE_DOCKER # If runs with containers [ yes ]
IPYTHONDIR # Folder to save autofiles of IPython [ /app/.ipython ]

# Redis
# ------------------------------------------------------------------------------
REDIS_URL # Redis URL [ redis://redis:6379/0 ]

# Celery
# ------------------------------------------------------------------------------
CELERY_BROKER_URL # Usually is redis so is the same URL [ redis://redis:6379/0 ]

# Flower
CELERY_FLOWER_USER # User for fower web [ celery_user ]
CELERY_FLOWER_PASSWORD # Password for flower web [ celery_password ]

# Apps
# ------------------------------------------------------------------------------
PTS_DASHBOARD_URL # URL shared to insert into HTML iframe
QUALITY_DASHBOARD_URL # URL shared to insert into HTML iframe
```

<br/>

Envs for _PostgreSQL_ - **./.envs/postgres.local.env**

```bash
POSTGRES_HOST # PostgreSQL host [ localhost ]
POSTGRES_PORT # PostgreSQL posrt [ 5432 ]
POSTGRES_DB # Database name [ systemtest ]
POSTGRES_USER # Database user [ postgres_user ]
POSTGRES_PASSWORD # Database password [ postgres_password ]
```

</details>

<br/>

### Envs - Production

<details>
<summary> envs </summary>

Envs for _Django_ - **./envs/.django.production.env**

```bash
# General
# ------------------------------------------------------------------------------
DJANGO_SETTINGS_MODULE # Django settings module [ config.settings.production ]
DJANGO_SECRET_KEY # Random string to creates HASHES [ QtpaNdY6A8Wq6KlnhdsO1t ]
DJANGO_ADMIN_URL # URL to access to adminsite [ admin/ ]
DJANGO_ALLOWED_HOSTS # Wildcard * to allow all IPs [ * ]

# Security
# ------------------------------------------------------------------------------
# TIP: better off using DNS, however, redirect is OK too
DJANGO_SECURE_SSL_REDIRECT # If redirects all HTTP to HTTPS [ False ]

# Redis
# ------------------------------------------------------------------------------
REDIS_URL # Redis URL [ redis://redis:6379/0 ]

# Celery
# ------------------------------------------------------------------------------
CELERY_BROKER_URL # Usually is redis so is the same URL [ redis://redis:6379/0 ]

# Flower
CELERY_FLOWER_USER # User for fower web [ celery_user ]
CELERY_FLOWER_PASSWORD # Password for flower web [ celery_password ]

# Apps
# ------------------------------------------------------------------------------
PTS_DASHBOARD_URL # URL shared to insert into HTML iframe
QUALITY_DASHBOARD_URL # URL shared to insert into HTML iframe
```

<br/>

Envs for _PostgreSQL_ - **./envs/.postgres.production.env**

```bash
POSTGRES_HOST # PostgreSQL host [ localhost ]
POSTGRES_PORT # PostgreSQL posrt [ 5432 ]
POSTGRES_DB # Database name [ systemtest ]
POSTGRES_USER # Database user [ postgres_user ]
POSTGRES_PASSWORD # Database password [ postgres_password ]
```

<br/>

Envs for _IBM DB2_ - **./envs/.db2.production.env**

```bash
DB2_HOST # DB2 host [ localhost ]
DB2_PORT # DB2 posrt [ 50000 ]
DB2_DB # Database name [ Q9 ]
DB2_USER # Database user [ db2_user ]
DB2_PASSWORD # Database password [ db2_password ]
DB2_PROTOCOL= # Protocol to make connection [ TCPIP ]
```

</details>
<br/>

## Run

### Run - Local

```bash
docker-compose -p project_name -f containers/local.yml up -d
```

<br/>

### Run - Production

```bash
podman-compose -p project_name -f containers/production.yml up -d
```

<br/>

## Update

### Update - Local

```bash
docker-compose -p project_name -f containers/local.yml up -d --build
```

### Update - Production

```bash
podman-compose -p project_name -f containers/production.yml up -d --build
```
<br/>

## Links & References

- [Docker][docker]
- [Docker Dockerfile][docker-dockerfile]
- [Docker Compose][docker-compose]
- [Docker Compose Up][docker-compose-up]
- [Django][django-docs]
- [Celery][celery-docs]
- [PostgersSQL][postgresql]
- [IBM DB2][ibmdb-docs]

<br/>

## License

![license logo]

PowerTest _SystemTest Web Applications_ is [BSD-3 licenced][license]

<br/>

## Author

### @AlanVazquez alan.vazquez.pacheco@ibm.com

<!-- Reference links -->
[pytz]: https://github.com/stub42/pytz
[python-slugify]: https://github.com/un33k/python-slugify
[pillow]: https://github.com/python-pillow/Pillow
[argon2]: https://github.com/hynek/argon2_cffi
[whitenoise]: https://github.com/evansd/whitenoise
[redis-py]: https://github.com/andymccurdy/redis-py
[hiredis]: https://github.com/redis/hiredis-py
[uvicorn]: https://github.com/encode/uvicorn
[ibmdb]: https://github.com/ibmdb/python-ibmdb
[psycopg2]: https://github.com/psycopg/psycopg2
[celery]: https://github.com/celery/celery
[celery-beat]: https://github.com/celery/django-celery-beat
[celery-timezone]: https://github.com/celery/django-celery-beat/pull/378
[flower]: https://github.com/mher/flower
[environ]: https://github.com/joke2k/django-environ
[werkzeug]: https://github.com/pallets/werkzeug
[ipdb]: https://github.com/gotcha/ipdb
[watchdog]: https://github.com/samuelcolvin/watchgod
[pylint-django]: https://github.com/PyCQA/pylint-django
[pylint-celery]: https://github.com/PyCQA/pylint-celery
[toolbar]: https://github.com/jazzband/django-debug-toolbar
[django-redis]: https://github.com/jazzband/django-redis
[django-extensions]: https://github.com/django-extensions/django-extensions
[gunicorn]: https://github.com/benoitc/gunicorn
[django]: https://www.djangoproject.com/

[docker]: https://docs.docker.com/reference/
[docker-dockerfile]: https://docs.docker.com/engine/reference/builder/
[docker-compose]: https://docs.docker.com/compose/compose-file/compose-file-v3/
[docker-compose-up]: https://docs.docker.com/compose/reference/up/
[django-docs]: https://docs.djangoproject.com/en/3.1/
[celery-docs]: https://docs.celeryproject.org/en/v4.4.7/getting-started/introduction.html
[postgresql]: https://www.postgresql.org/docs/13/index.html
[ibmdb-docs]: https://github.com/ibmdb/python-ibmdb/wiki/APIs

<!-- badges -->
[python]: https://img.shields.io/badge/python%20-%2314354C.svg?&style=for-the-badge&logo=python&logoColor=white
[postgres]: https://img.shields.io/badge/postgres-%23316192.svg?&style=for-the-badge&logo=postgresql&logoColor=white
[django-logo]: https://img.shields.io/badge/django%20-%0c4b33.svg?&style=for-the-badge&logo=django&logoColor=white&color=0c4b33
[celery-logo]: https://img.shields.io/badge/celery%20-%b6de64.svg?&style=for-the-badge&logo=celery&logoColor=white&color=b6de64
[docker-logo]: https://img.shields.io/badge/docker%20-%2314354C.svg?&style=for-the-badge&logo=docker&logoColor=white&color=2496ed
[podman-logo]: https://img.shields.io/badge/podman%20-%2314354C.svg?&style=for-the-badge&logo=podman&logoColor=white&color=892ca0
[redis-logo]: https://img.shields.io/badge/redis%20-%2314354C.svg?&style=for-the-badge&logo=redis&logoColor=white&color=e92c00

<!-- Other Links -->

[license]: https://tldrlegal.com/license/bsd-3-clause-license-(revised) "License descriptions"
[license logo]: https://img.shields.io/pypi/l/Django?style=for-the-badge
