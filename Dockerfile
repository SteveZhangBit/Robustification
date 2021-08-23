FROM python:3.8

RUN set -ex; apt-get update \
    && apt-get install -y --no-install-recommends \
        git \
        openjdk-11-jdk \
        libcairo2-dev \
        pkg-config \
        python3-dev \
    && pip install poetry

COPY lts.py repair.py /Robustification/
COPY bin /Robustification/bin/
COPY lib /Robustification/lib/
COPY models /Robustification/models/

WORKDIR /Robustification/lib
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi \
    && poetry shell

WORKDIR /Robustification/models

CMD ["bash"]
