# Сервис асинхронного API для онлайн кинотеатра

ETL: https://github.com/LoburYaroslav/new_admin_panel_sprint_3

## Разработка

1. Установить зависимости из `dev-requirements.txt` (включают в себя requirements.txt):

```shell
pip install -r dev-requirements.txt
```

2. Добавить пре-коммит хуки:

```shell
pre-commit install
```

## .env

В проекте есть файл `.env.example` в нем - примеры переменных среды. Для разработки необходимо рядом завести файл `.env` и указать в нем все
необходимые переменные среды. Этот файл игнорится гитом. А так же на него смотрит `docker-compose.yml`

## Запуск

Для сборки и запуска запустить:

```shell
 docker-compose up --build -d
```
