# ---------- Stage 1: Builder ----------
FROM python:3.9-slim-bookworm AS builder

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=2.2.1 \
    VENV_PATH=/opt/venv

RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc make build-essential curl \
    && python -m venv --copies $VENV_PATH \
    && $VENV_PATH/bin/pip install --upgrade pip \
    && $VENV_PATH/bin/pip install "poetry==$POETRY_VERSION" poetry-plugin-export \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="$VENV_PATH/bin:$PATH"
WORKDIR /build

COPY pyproject.toml poetry.lock* ./

RUN poetry export -f requirements.txt --without-hashes -o requirements.txt && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache

# ---------- Stage 2: Runtime ----------
FROM python:3.9-slim-bookworm AS runtime

COPY --from=builder /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONPATH="/app" \
    APP_SETTINGS=production

RUN mkdir -p /app /var/log/app && \
    chmod -R g+rwX /app /var/log/app /opt/venv && \
    chgrp -R 0 /app /var/log/app /opt/venv

WORKDIR /app
COPY . /app/users

RUN rm -rf /app/users/{pyproject.toml,poetry.lock,Makefile,deploy} \
    && find / -type d -name "__pycache__" -exec rm -rf {} + \
    && rm -rf /root/.cache /var/cache/*

USER 1001

EXPOSE 8000
ENTRYPOINT ["gunicorn", "--config", "/app/users/config.py", "users.app:APP"]
