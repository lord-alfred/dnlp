FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11-slim

# lint it:
# $ docker run --rm -i hadolint/hadolint < Dockerfile

# hadolint ignore=DL3008
RUN apt-get update -y && apt-get install -y --no-install-recommends git gcc g++ curl && rm -rf /var/lib/apt/lists/*
# hadolint ignore=DL3013
RUN pip install --no-cache-dir --upgrade pip

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# for fasttext pretrained model & nltk tokenizers
ENV MODEL_PATH=/fasttext/lid.176.bin
RUN mkdir -p /fasttext && mkdir -p /root/nltk_data

VOLUME ["/fasttext"]
VOLUME ["/root/nltk_data"]

COPY ./src/dnlp /app
COPY ./prestart.sh /app
