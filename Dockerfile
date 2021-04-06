FROM python:3.9-alpine

# hadolint ignore=DL3018
RUN apk update && apk --no-cache add git gcc g++ curl python3-dev make automake

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

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
