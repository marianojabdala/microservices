FROM python:alpine3.6

RUN apk add --update python-dev py-pip gcc linux-headers musl-dev libffi-dev postgresql-dev && \
    mkdir /app

WORKDIR app

COPY requirements.txt /app

RUN pip install -r requirements.txt

ARG APP_SETTINGS=production

ENV APP_SETTINGS $APP_SETTINGS

EXPOSE 8000

COPY . /app

RUN adduser -S app && chown app:nobody -R /app && \
    apk del gcc linux-headers musl-dev libffi-dev&& \
    rm /var/cache/apk/*

USER app

ENTRYPOINT ["gunicorn" ,"--config", "config.py", "app:app"]


