FROM python:3.9

COPY requirements.txt /temp/requirements.txt
COPY store /store
WORKDIR /store
# WORKDIR - для того чтобы когда мы какие-то команды передавали внутрь контейнера, то они запускались из этой директории, из той где лежит Django приложение
# то есть не нужно будет писать полный путь до файла manage.py, будем запускать из той папки где этот файл manage.py находится
EXPOSE 8000

# для FROM python:3.9-alpine...
#RUN apk add build-base postgresql-dev postgresql-client
# эти три пакета (зависимости) нужны установить в Linux для подключения python к postgres
# для FROM python:3.9
# postgresql-dev аналогом для python:3.9 будет libpq-dev
# build-base аналогом для python:3.9 будет build-essential, но убрал ее
RUN apt-get update && apt-get install -y postgresql-client libpq-dev

RUN pip install -r /temp/requirements.txt
# -r показывает из какого файла надо произвести установку зависимостей

RUN adduser --disabled-password store-user
# adduser создает юзера| --disabled-password не нужен пароль, тк к контейнеру имею доступ только я| store-user это имя юзера

USER store-user
# создаем юзера чтобы не под root заходить, а от имени юзера выполнять все команды


# build-base, то его аналог в обычном образе (не alpine)-библиотека build-essential
# аналог postgresql-dev - libpq-dev
# build-essential, он для сборки пакетов Debian, а так как у меня Image python:3.9 (он в отличие от Alpine собирается на основе Image Debian), то он возможно и не нужен
# libpq-dev - содержит набор функций, используя которые клиентские программы (C++, Perl, Python...) могут передавать запросы серверу PostgreSQL и принимать результаты этих запросов

