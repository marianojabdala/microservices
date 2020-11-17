FROM python:3.7-slim as build-base

LABEL maintainer="marianoabdala@gmail.com"

RUN apt update && apt install -y --no-install-recommends gcc make wget python3-dev libffi-dev && \
    python -m venv /opt/venv && \
    pip install pip --upgrade && \
    pip install pipenv
    
ENV PATH="/opt/venv/bin:$PATH"

FROM build-base as intermediate-build

COPY requirements.txt .

RUN pip install -r requirements.txt

FROM python:3.7-slim as release-image

COPY --from=intermediate-build /opt/venv /opt/venv

ARG APP_SETTINGS=production

COPY . /app

RUN mkdir -p /var/log/app/ && \
    addgroup --system appgroup  && \
    adduser --system app && usermod -aG appgroup app && \
    chown app:appgroup -R /app && \
    chown app:appgroup -R /var/log/app/ && \
    apt autoremove -y && \
    rm -fr /app/docker/  && \
    rm -fr /root/.cache /root/.local /var/cache/ && \
    find / -name "__pycache__" | xargs rm -fr

WORKDIR /app

ENV APP_SETTINGS=$APP_SETTINGS \
    PATH="/opt/venv/bin:/app:$PATH"

USER app

EXPOSE 5000

ENTRYPOINT ["gunicorn" ,"--config", "config.py", "app:APP"]