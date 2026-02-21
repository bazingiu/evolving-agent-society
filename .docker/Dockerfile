FROM python:3.12-slim
WORKDIR /app

RUN pip install uv

COPY pyproject.toml .
RUN uv pip install --system -e ".[dev]"

COPY src/ ./src/

ENV PYTHONPATH=/app/src

CMD ["python", "scripts/run_local.py"]