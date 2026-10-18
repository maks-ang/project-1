FROM python:3.14.0

WORKDIR /app

RUN pip install uv

COPY . .

RUN uv sync

CMD ["/app/.venv/bin/python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]