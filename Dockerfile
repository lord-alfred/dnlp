FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11-slim

# lint it:
# $ docker run --rm -i hadolint/hadolint < Dockerfile

# hadolint ignore=DL3008
RUN apt-get update -y && apt-get install -y --no-install-recommends git gcc g++ curl && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# download fasttext pretrained model
RUN mkdir -p /fasttext && curl -L https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin > /fasttext/lid.176.bin
ENV MODEL_PATH=/fasttext/lid.176.bin

# download nltk punkt
RUN python -c "import nltk; nltk.download('punkt')"

VOLUME ["/fasttext"]
VOLUME ["/root/nltk_data"]

COPY ./app /app
