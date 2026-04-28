FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

COPY shared/requirements.txt ./shared-requirements.txt
RUN pip install --no-cache-dir -r shared-requirements.txt

COPY api-gateway/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY shared/ /app/shared/
COPY api-gateway/ /app/api_gateway/

ENV PYTHONPATH=/app

EXPOSE 8004

CMD ["uvicorn", "api_gateway.main:app", "--host", "0.0.0.0", "--port", "8004"]