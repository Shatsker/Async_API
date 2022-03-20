# Проектная работа 4 спринта

**Важное сообщение для тимлида:** для ускорения проверки проекта укажите ссылку на приватный репозиторий с командной работой в файле readme
и отправьте свежее приглашение на аккаунт [BlueDeep](https://github.com/BigDeepBlue).

В папке **tasks** ваша команда найдёт задачи, которые необходимо выполнить в первом спринте второго модуля. Обратите внимание на задачи **
00_create_repo** и **01_create_basis**. Они расцениваются как блокирующие для командной работы, поэтому их необходимо выполнить как можно
раньше.

Мы оценили задачи в стори поинтах, значения которых брались
из [последовательности Фибоначчи](https://ru.wikipedia.org/wiki/Числа_Фибоначчи) (1,2,3,5,8,…).

Вы можете разбить имеющиеся задачи на более маленькие, например, распределять между участниками команды не большие куски задания, а
маленькие подзадачи. В таком случае не забудьте зафиксировать изменения в issues в репозитории.

**От каждого разработчика ожидается выполнение минимум 40% от общего числа стори поинтов в спринте.**

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