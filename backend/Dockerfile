FROM python:3.11-slim

ENV PYTHONPATH=/app
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
	PIP_NO_CACHE_DIR=1 \
	PYTHONDONTWRITEBYTECODE=1
WORKDIR /app

RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt requirements.txt
RUN python -m pip install --upgrade pip \
	&& python -m pip install -r requirements.txt

COPY backend/ /app/backend/
COPY scripts/ /app/scripts/

EXPOSE 8000

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
