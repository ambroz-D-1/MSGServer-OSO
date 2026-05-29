FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

FROM base AS build

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

FROM build AS dep

ARG GIT_REPO=https://github.com/ambroz283878/MSGServer-OSO

RUN git clone ${GIT_REPO} .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM base AS run

COPY --from=dep /install /usr/local
COPY --from=dep /app /app

CMD ["python", "server.py"]