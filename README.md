# dNLP

Сборник полезных штук из Natural Language Processing, завернутый в API в виде Docker-контейнера.

## Содержимое dNLP

В данный момент в состав входит:
1. **Определение языка текста** – за основу взята библиотека [fastText](https://fasttext.cc/) с её предобученной моделью для распознавания 176 языков.
2. **Разделение текста на предложения** – за основу взяты токенайзеры от [NLTK](https://www.nltk.org/).

## Установка Docker

Примеры ниже для Ubuntu, установка под привелигерованным пользователем (root).

Установка docker:
```shell script
apt-get remove docker docker-engine docker.io containerd runc
apt-get update
apt-get install apt-transport-https ca-certificates curl gnupg lsb-release
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
apt-get update
apt-get install docker-ce docker-ce-cli containerd.io git
```

Установка docker-compose:
```shell script
curl -L "https://github.com/docker/compose/releases/download/1.28.6/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```

Подробная документация:
1. https://docs.docker.com/engine/install/ubuntu/
2. https://docs.docker.com/compose/install/

## Запуск dNLP

Вначале склонируем репу:
```shell script
git clone https://github.com/lord-alfred/dnlp.git
```

И непосредственно запустим контейнер:
```shell script
cd dnlp
docker-compose up --build -d
```

## Проверка работоспособности

После запуска _на той же машине_ можно стрельнуть в контейнер запросами:
```shell script
# проверка определения языка:
curl -v -XPOST -d 'text=some+useful+info' http://127.0.0.1:9090/detect-language

# провера токенизации:
curl -v -XPOST -d 'text=Test+sent%3F+Don%27t+or+ms.+Not%21+Yes%2C+of+course.+Maybe+mr.Jeck+and+band.&lang=en' http://127.0.0.1:9090/tokenize-sentences
```

Для проверки с другого сервера – нужно поменять IP адрес и убедиться что во встроенном фаерволле не закрыт порт `9090`.

## Входные и выходные параметры

Все эндпоинты обрабатывают только запросы с HTTP метода `POST`.

API Endpoint для определение языка текста поддерживает следующие входные параметры:
- `text` – строка с текстом, у которой нужно определить язык;
- `count` – количество результатов. По дефолту: `3`.

В результате будет json в виде массива словарей:
```json
[
  {
    "confidence": 0.5937589406967163,
    "code": "en",
    "name": "English",
    "family": "Indo-European",
    "endonym": "English",
    "iso639-1": "en",
    "iso639-2/T": "eng",
    "iso639-2/B": "eng",
    "iso639-3": "eng"
  }
]
```

API Endpoint для разделения текста на предложения поддерживает следующие входные параметры:
- `text` – строка с текстом, которую нужно разбить на предложения;
- `lang` – код язык текста. По дефолту: `en`.

Поддерживаемые языки для токенизации:
```
{
    'en': 'english',
    'ru': 'russian',
    'cs': 'czech',
    'da': 'danish',
    'nl': 'dutch',
    'et': 'estonian',
    'fi': 'finnish',
    'fr': 'french',
    'de': 'german',
    'el': 'greek',
    'it': 'italian',
    'no': 'norwegian',
    'pl': 'polish',
    'pt': 'portuguese',
    'sl': 'slovene',
    'es': 'spanish',
    'sv': 'swedish',
    'tr': 'turkish',
}
```

В результате будет json в виде массива строк:
```json
[
  "Test sent?",
  "Don't or ms. Not!",
  "Yes, of course.",
  "Maybe mr.Jeck and band."
]
```

# Автор

Lord_Alfred

Блог: [https://t.me/lord_Alfred](https://t.me/lord_Alfred)
