FROM python:3.11-slim

WORKDIR /app

COPY shared/requirements.txt ./shared-requirements.txt
RUN pip install --no-cache-dir -r shared-requirements.txt

COPY api-gateway/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY shared/ /app/shared/
COPY api-gateway/ /app/api-gateway/

ENV PYTHONPATH=/app

EXPOSE 8004

CMD ["uvicorn", "api-gateway.main:app", "--host", "0.0.0.0", "--port", "8004"]