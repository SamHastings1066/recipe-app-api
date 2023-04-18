FROM python:3.9-alpine3.13
LABEL maintainer="Sam Hastings"

ENV PYTHONUNBUFFERED 1

# Copy requirements.txt from our local machine into the Docker image.
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
# Copy app directory into the Docker container
COPY ./app /app
# Set the working directory - the directory that commands are run from when we
# run commands on our DOcker image. /app is the location where our Django
# project is synced to, so we don't need to specify the full path of the
# Django Managment Command.
WORKDIR /app
# Expose port 8000 from our container to our machine when we run our container.
# This allows us to connect to the Django development server
EXPOSE 8000


ARG DEV=false
RUN python -m venv /py && \
  /py/bin/pip install --upgrade pip && \
  apk add --update --no-cache postgresql-client && \
  apk add --update --no-cache --virtual .tmp-build-deps \
    build-base postgresql-dev musl-dev && \
  /py/bin/pip install -r /tmp/requirements.txt && \
  if [ $DEV = "true" ]; \
    then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
  fi && \
  rm -rf /tmp && \
  apk del .tmp-build-deps && \
  adduser \
    --disabled-password \
    --no-create-home \
    django-user

ENV PATH="/py/bin:$PATH"

USER django-user
