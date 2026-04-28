FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

COPY shared/requirements.txt ./shared-requirements.txt
RUN pip install --no-cache-dir -r shared-requirements.txt

COPY project-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY shared/ /app/shared/
COPY project-service/ /app/project_service/

ENV PYTHONPATH=/app

EXPOSE 8002

CMD ["uvicorn", "project_service.main:app", "--host", "0.0.0.0", "--port", "8002"]