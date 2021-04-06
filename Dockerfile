FROM python:3.9

# lint it:
# $ docker run --rm -i hadolint/hadolint < Dockerfile

# hadolint ignore=DL3018
RUN apt-get update -y && apt-get install -y --no-install-recommends git gcc g++ curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# download fasttext pretrained model
VOLUME ["/fasttext"]
RUN mkdir -p /fasttext && curl -L https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin > /fasttext/lid.176.bin
ENV MODEL_PATH=/fasttext/lid.176.bin

# download nltk punkt
VOLUME ["/root/nltk_data"]
RUN python -c "import nltk; nltk.download('punkt')"

COPY . /app
RUN pip install -e .

CMD ["dnlp"]
