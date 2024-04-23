# Dockerfile
# Uses multi-stage builds requiring Docker 17.05 or higher
# See https://docs.docker.com/develop/develop-images/multistage-build/

# Creating a python base with shared environment variables
FROM python:3.9.13-slim-bullseye AS python-base

ARG PIP_NO_CACHE_DIR=off
ARG PIP_DISABLE_PIP_VERSION_CHECK=on
ARG PIP_DEFAULT_TIMEOUT=100
ARG POETRY_HOME="/opt/poetry"
ARG POETRY_VIRTUALENVS_IN_PROJECT=true
ARG POETRY_NO_INTERACTION=1
ARG PYSETUP_PATH="/opt/pysetup"
ARG POETRY_VERSION=1.5.1
ARG VENV_PATH="/opt/pysetup/.venv"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=$PYTHONUNBUFFERED \
    PIP_DISABLE_PIP_VERSION_CHECK=$PIP_DISABLE_PIP_VERSION_CHECK \
    PIP_DEFAULT_TIMEOUT=$PIP_DEFAULT_TIMEOUT \
    POETRY_HOME=$POETRY_HOME \
    POETRY_VIRTUALENVS_IN_PROJECT=$POETRY_VIRTUALENVS_IN_PROJECT \
    POETRY_NO_INTERACTION=$POETRY_NO_INTERACTION \
    PYSETUP_PATH=$PYSETUP_PATH \
    VENV_PATH=$VENV_PATH \
    POETRY_VERSION=$POETRY_VERSION

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# builder-base is used to build dependencies
FROM python-base AS builder-base
RUN buildDeps="build-essential" \
    && apt-get update \
    && apt-get install --no-install-recommends -y \
    curl \
    vim \
    netcat \
    && apt-get install -y --no-install-recommends $buildDeps \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry - respects $POETRY_VERSION & $POETRY_HOME
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=${POETRY_HOME} python3 - --version ${POETRY_VERSION} \
    && chmod a+x /opt/poetry/bin/poetry

# We copy our Python requirements here to cache them
# and install only runtime deps using poetry
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./
RUN poetry install --only main

# 'production' stage uses the clean 'python-base' stage and copyies
# in only our runtime deps that were installed in the 'builder-base'
FROM python-base AS production
ENV FASTAPI_ENV=production

COPY --from=builder-base $VENV_PATH $VENV_PATH
COPY gunicorn_conf.py ./gunicorn_conf.py

COPY docker-entrypoint.sh ./docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Create user with the name poetry
RUN groupadd -g 1500 poetry && \
    useradd -m -u 1500 -g poetry poetry

COPY --chown=poetry:poetry ./app /app
USER poetry
WORKDIR /app

# Open port 8000 for communication
EXPOSE 8000

ENTRYPOINT /docker-entrypoint.sh $0 $@
CMD [ "gunicorn", "--worker-class uvicorn.workers.UvicornWorker", "--config /gunicorn_conf.py", "main:app"]

