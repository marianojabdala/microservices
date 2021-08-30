FROM python:3.9-slim as build-base

LABEL maintainer="marianoabdala@gmail.com"
LABEL user.microservice.version="0.1.0"

RUN apt update && apt install -y --no-install-recommends gcc make wget python3-dev && \
    python -m venv --copies /opt/venv && \
    pip install pip --upgrade && \
    pip install poetry
    
ENV PATH="/opt/venv/bin:$PATH"

FROM build-base AS intermediate-build

COPY pyproject.toml /tmp
RUN cd /tmp && \
    poetry export -o requirements.txt --without-hashes && \
    chmod +x /opt/venv/bin/activate && \
    /opt/venv/bin/activate && pip install -r requirements.txt && \
    rm /tmp/pyproject.toml

FROM python:3.9-slim as release-image

ARG APP_SETTINGS=production

COPY --from=intermediate-build /opt/venv /opt/venv

COPY . /app/users

RUN mkdir -p /var/log/app/ && \
    addgroup --system appgroup  && \
    adduser --system app --no-create-home && usermod -aG appgroup app && \
    chown app:appgroup -R /app && \
    chown app:appgroup -R /var/log/app/ && \
    rm -fr /app/users/deploy  && \
    rm -fr /app/users/poetry.lock /app/users/pyproject.toml /app/users/Makefile && \
    rm -fr /root/.cache /root/.local /var/cache/ && \
    find / -name "__pycache__" | xargs rm -fr

WORKDIR /app

ENV APP_SETTINGS=$APP_SETTINGS \
    PATH="/opt/venv/bin:/app:/app/users:$PATH" \
    PYTHONPATH="../"

USER app

EXPOSE 8000

ENTRYPOINT ["/opt/venv/bin/gunicorn" ,"--config", "/app/users/config.py", "users.app:APP"]
