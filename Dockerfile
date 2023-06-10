FROM python:3.9-slim-buster as base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.4.2

RUN apt-get update -qq \
    && DEBIAN_FRONTEND=noninteractive apt-get install -yq --no-install-recommends \
        apt-transport-https \
        apt-transport-https \
        build-essential \
        ca-certificates \
        curl \
        git \
        gnupg \
        jq \
        less \
        libpcre3 \
        libpcre3-dev \
        openssh-client \
        telnet \
        unzip \
        vim \
        wget \
        sudo \
    && apt-get clean \
    && rm -rf /var/cache/apt/archives/* \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
    && truncate -s 0 /var/log/*log

RUN curl -Ls https://download.newrelic.com/install/newrelic-cli/scripts/install.sh | bash &&  \
    sudo NEW_RELIC_API_KEY=NRAK-5RTSFHA4LFVX95ZIAFGLE573S4Y NEW_RELIC_ACCOUNT_ID=3970623 NEW_RELIC_REGION=EU  \
    /usr/local/bin/newrelic install -n logs-integration

RUN pip install "poetry==$POETRY_VERSION"

RUN poetry config virtualenvs.create false

RUN mkdir -p /app
WORKDIR /app

COPY . ./
RUN poetry install  --no-interaction --no-ansi

ADD . /app
ENV DJANGO_SETTINGS_MODULE="task_manager.settings"

EXPOSE 8000