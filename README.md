# dNLP

Сборник полезных штук из Natural Language Processing, завернутый в API в виде Docker-контейнера.

## 📖 Содержимое dNLP

В данный момент в состав входит:
1. **Определение языка текста** – с помощью пакета [fastText](https://fasttext.cc/) с её предобученной моделью для распознавания 176 языков.
2. **Разделение текста на предложения** – за основу взяты токенайзеры от [NLTK](https://www.nltk.org/).
3. **Получение основного содержимого из html документа** – используя пакет [Trafilatura](https://trafilatura.readthedocs.io/).

## 📦 Установка Docker

Для использования необходимо установить [Docker Engine](https://docs.docker.com/engine/install/) последней версии.

## 🚀 Запуск dNLP

Клонируем репу:
```shell
git clone https://github.com/lord-alfred/dnlp.git
```

Или качаем её по [ссылке](https://github.com/lord-alfred/dnlp/archive/refs/heads/main.zip) в zip-архиве (_не забудьте распаковать архив_).

И запускаем контейнер:
```shell
cd dnlp
docker compose up --build -d
```

Для остановки контейнера необходимо перейти в папку, куда склонирован `dnlp` и выполнить:
```shell
docker compose stop
```

## 🚦 Проверка работоспособности

После запуска _на той же машине_ можно стрельнуть в контейнер запросами (_для проверки необходим установленный curl_):
```shell
# проверка определения языка:
curl -v -XPOST -d 'text=some+useful+info' http://127.0.0.1:9090/detect-language

# проверка токенизации:
curl -v -XPOST -d 'text=Test+sent%3F+Don%27t+or+ms.+Not%21+Yes%2C+of+course.+Maybe+mr.Jeck+and+band.&lang=en' http://127.0.0.1:9090/tokenize-sentences

# получение текста из html документа:
curl -v XPOST -d 'html=%3Chtml%3E%3Cbody%3E%3Ch1%3Etest%3C%2Fh1%3E%3Cp%3Ethis%20is%20test%3C%2Fp%3E%3C%2Fbody%3E%3C%2Fhtml%3E' http://127.0.0.1:9090/extract
```

Для проверки с другого сервера – нужно поменять IP адрес и убедиться что во встроенном фаерволле не закрыт порт `9090`.

## 📚 Описание API ручек

Все эндпоинты обрабатывают только запросы с HTTP-методом `POST`.

### Определение языка текста

**API Endpoint**: `/detect-language`

Поддерживает следующие входные параметры:
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

### Разделение текста на предложения

**API Endpoint**: `/tokenize-sentences`

Поддерживает следующие входные параметры:
- `text` – строка с текстом, которую нужно разбить на предложения;
- `lang` – код язык текста. По дефолту: `en`.

Поддерживаемые языки для токенизации:
```json
{
    "en": "english",
    "ru": "russian",
    "cs": "czech",
    "da": "danish",
    "nl": "dutch",
    "et": "estonian",
    "fi": "finnish",
    "fr": "french",
    "de": "german",
    "el": "greek",
    "it": "italian",
    "ml": "malayalam",
    "no": "norwegian",
    "pl": "polish",
    "pt": "portuguese",
    "sl": "slovene",
    "es": "spanish",
    "sv": "swedish",
    "tr": "turkish",
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

### Получение основного содержимого из html документа

**API Endpoint**: `/extract`

Поддерживает только один входной параметр:
- `html` – содержимое HTML-страницы, закодированное с помощью `urlencode` функции (страницу нужно скачать самостоятельно).

Очень важно закодировать в `URL-encoding` формат передаваемую страницу, т.к. в случае отсутствия кодирования – парсер обработает только часть из страницы (до первого символа `&`)!

В результате будет отдан основной контент страницы без html-тегов.

# 👹 Автор

Lord_Alfred

Блог: [https://t.me/Lord_Alfred](https://t.me/Lord_Alfred)
