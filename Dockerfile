FROM python:3.8-slim

# service port
EXPOSE 5000/tcp

# Buffer the Python environment
ENV PYTHONUNBUFFERED 1

# Keeps python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# install ab
RUN apt-get update && \
    apt-get install -y apache2-utils && \
    apt-get install -y apache2

# install poerty
RUN pip3 install --upgrade pip && \
    pip3 install poetry

# install dependencies
COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# install docker client, ping and curl.
RUN apt-get update && apt-get install -y \
    docker.io \
    iputils-ping \
    curl

# set workdir
WORKDIR /root/test

# copy app
COPY . .
