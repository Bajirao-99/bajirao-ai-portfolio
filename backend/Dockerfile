FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV HF_HOME=/app/.cache/huggingface

WORKDIR /app

RUN addgroup --system appgroup \
    && adduser \
        --system \
        --ingroup appgroup \
        appuser

COPY requirements.txt .

RUN python -m pip install \
        --upgrade pip \
    && pip install \
        --no-cache-dir \
        -r requirements.txt

COPY . .

RUN mkdir -p \
        /app/uploads \
        /app/.cache/huggingface \
    && chown -R \
        appuser:appgroup \
        /app

USER appuser

EXPOSE 8000

CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]