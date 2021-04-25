
FROM python:3.9

ENV PYTHONUNBUFFERED 1

RUN addgroup --system django \
  && adduser --system --ingroup django django

COPY ./containers/django/commands /commands
RUN chmod +x /commands/*

COPY ./requirements /requirements
RUN pip install --no-cache-dir -r /requirements/production.txt \
  && rm -rf /requirements

COPY --chown=django:django . /app

USER django

WORKDIR /app

ENTRYPOINT ["/commands/entrypoint.sh"]
