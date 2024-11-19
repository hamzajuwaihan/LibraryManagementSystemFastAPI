# syntax=docker/dockerfile:1.3
FROM python:3.11-slim AS base

FROM base AS build

ENV PATH=/opt/local/bin:$PATH \
    PIP_PREFIX=/opt/local \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get update && \
    apt-get install -y \
    libpq-dev gcc make


WORKDIR /tmp

COPY requirements.txt .
RUN pip install -r requirements.txt

FROM base AS deploy

ENV PATH=/opt/local/bin:$PATH \
    PYTHONPATH=/opt/local/lib/python3.11/site-packages:/app

COPY --from=build /opt/local /opt/local
COPY --from=build /usr/lib/x86_64-linux-gnu/ /lib/x86_64-linux-gnu/ /usr/lib/

WORKDIR /app
COPY . /app

EXPOSE 80

STOPSIGNAL SIGINT

CMD ["sh","bin/boot.sh"]
