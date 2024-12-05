FROM python:3.11-alpine3.19 AS build

RUN apk add build-base libpq libpq-dev

COPY ./requirements.txt ./

RUN pip3 install --no-cache-dir -r ./requirements.txt


FROM python:3.11-alpine3.19 AS final

ENV APP_HOME=/app

RUN apk update \
    && apk upgrade \
    && apk add bash

# Встановимо робочу директорію всередині контейнера
WORKDIR $APP_HOME

COPY . .
COPY --from=build /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/

CMD ["python3", "get_report.py"]