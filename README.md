# ML Final Task

## Описание файлов

**final.ipynb** - notebook в котором происходит обработка датасета, обучение и тестирование модели

**source_datasets** - папка с двумя датасетами, которые легли в основу обучающего датасета (после предобработки) - SpamAssasin и LingSpam

**two_datasets.csv** - базовый датасет, используемый для обучения и валидации модели (представляет из себя комбинацию датасетов из папки source_datasets после дополнительной обработки)

**result.csv** - преобразованный из набора .eml файлов писем электронной почты в CSV файл с колонками Message и Spam тестовый датасет (предлагаемый для оценки точности)

**create_dataset.py** - скрипт на Python, который использовался для преобразования датасетов из source_datasets, а также тестового датасета в единый формат (Message, Spam колонки в CSV формате) из .eml файлов электронной почты

**base_config.cfg** - базовый конфиг-файл используемый библиотекой spaCy в котором заданы параметры обучения модели

**textcat_config.cfg** - расширенный конфиг-файл, сгенерированный библиотекой spaCy на основе базового и используемый библиотекой spaCy во время обучения модели

**output6/model-best** - папка, содержащая обученную модель с наилучшими показателями точности (на основе валидации при обучении)

**fastapi_server.py** - скрипт на Python, содержащий роут, в котором на вход запроса передается текст письма с электронной почты (параметр input_text), этот текст далее передается на вход обученной модели, а затем на выходе передается словарь с ключами SPAM, NOT SPAM (полученный из модели) и значениями от 0 до 1, характеризующими вероятность того, что письмо является (1) / не является (0) спамом.

**Dockerfile** - докерфайл, в котором устанавливаются необходимые для работы FastAPI Python-зависимости, запускается FastAPI (через fastapi_server.py) с роутом, позволяющим произвести взаимодействие с обученной моделью.

**requirements.txt** - необходимые для работы FastAPI Python-зависимости

**LICENSE** - MIT-лицензия для безвозмездного и свободного использования/переиспользования проекта

## Варианты взаимодействия с моделью

### 1. Импорт в код другого проекта

Для использования модели в коде необходимо переместить в рабочую папку проекта (WORKDIR) папку output6/best-model, а также создать Python-окружение, в которое установить пакет spacy (пример для Linux/macOS):

```
cp -r output6/ WORKDIR && cd WORKDIR
python3 -m venv venv
source venv/bin/activate
pip install spacy==3.5.0
```

Далее в созданном Python-скрипте с помощью метода load() загрузить модель и передать ей на вход проверяемый текст(TEXT) в виде строки типа str, после чего получить результат в поле cats:

```
nlp = spacy.load('output6/model-best')
test_text = TEXT
doc = nlp(test_text)
doc.cats
```

Результатом doc.cats будет словарь с ключами SPAM, NOT SPAM и значениями вероятности от 0 д 1 принадлежности к данным классам.

### 2. Jupyter Notebook

Для работы с моделью посредством jupyter notebook необходимо установить в виртуальное Python-окружение пакет notebook:
```
python3 -m venv venv
source venv/bin/activate
pip install notebook
```

Затем открыть файл final.ipynb и выполнять необходимое взаимодействие. 

Минимальный набор файлов, необходимый для работы final.ipynb - конфиг-файл base_config.cfg, csv-датасет для обучения two_datasets.csv и тестирующий датасет result.csv

### 3. Fast API

Для использования модели через запросы к Fast API необходимо установить необходимые Python-зависимости в виртуальном Python-окружении (файл requirements.txt) и запустить FastAPI сервер:

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn fastapi_server:app --reload --host 0.0.0.0 --port 8000
```

Теперь можно производить к модели get запрос по адресу http://IP:8000/predict (где IP - внутренний/внешний IP адрес хоста, на котором выполняется запуск fastapi-сервера) и в ответ получать словарь с вероятностью отнесения / неотнесения письма к спаму.

### 4. Docker

Для использования модели через Docker-контайнер необходимо собрать Docker-образ с помощью Dockerfile и запустить его.

```
docker build . -t ml
docker run -p 8000:8000 ml
```

Теперь можно производить к модели get запрос по адресу http://IP:8000/predict (где IP - внутренний/внешний IP адрес хоста, на котором выполняется запуск fastapi-сервера) и в ответ получать словарь с вероятностью отнесения / неотнесения письма к спаму.

Докер-образ также доступен на DockerHub - https://hub.docker.com/repository/docker/ignatovskiy/ml/general
Для запуска готового образа с DockerHub можно использовать команду:

```
docker run ignatovskiy/ml
```

### 5. Telegram-бот

Взаимодействие с моделью для конечного пользователя также возможно через Telegram-бота @@ClassifySpamHSEBot
Необходимо отправить боту текст сообщения электронной почты, который необходимо проверить.

## Информация о модели

В основе модели лежит NLP-библиотека spaCy

Для решения задачи классификации текста используется TextCategorizer из spaCy (https://spacy.io/api/textcategorizer)

## Метрики модели

Accuracy: 94.32314410480349%

Results
|metric|value|
|-|-|
|TOK|                 100.00|
|TEXTCAT (macro F)|   93.98|
|SPEED|               39458|


Textcat F (per label)
|               |P       |R       |F|
|-|-|-|-|
SPAM|       96.12|   89.20|  92.53|
NOT SPAM|   93.29|   97.66|   95.42|


Textcat ROC AUC (per label)
|           |ROC AUC|
|-|-|
|SPAM|          0.98|
|NOT SPAM|     0.98|
