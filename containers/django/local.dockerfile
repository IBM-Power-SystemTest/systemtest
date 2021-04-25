FROM python:3.9

ENV PYTHONUNBUFFERED 1

COPY ./containers/django/commands /commands
RUN chmod +x /commands/*

COPY ./requirements /requirements
RUN pip install -r /requirements/local.txt

WORKDIR /app

ENTRYPOINT ["/commands/entrypoint.sh"]
