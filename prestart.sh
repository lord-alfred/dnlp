#!/usr/bin/env bash

set -eu
set -x

# download fasttext pretrained model
if [ ! -f "/fasttext/lid.176.bin" ]
then
    curl -L https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin > /fasttext/lid.176.bin
fi

# download nltk punkt
if [ ! -f "/root/nltk_data/tokenizers/punkt.zip" ]
then
    python3 -c "import nltk; nltk.download('punkt')"
fi
