# Dockerfile
# LangGraph Multi-Agent Research & Writing System

FROM python:3.12-slim

LABEL maintainer="Saeid Saadatigero <saeidsaadatigero@gmail.com>"
LABEL description="Multi-Agent Research & Writing System with LangGraph, LangChain, and LLM-as-Judge"
LABEL version="1.0.0"

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV APP_HOME=/app
WORKDIR $APP_HOME

# Copy requirements first (leverages Docker cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY main.py .
COPY .env.example .

# Security: non-root user
RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser $APP_HOME
USER appuser

CMD ["python", "main.py"]
