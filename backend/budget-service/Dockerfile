FROM python:3.11-slim

WORKDIR /app

COPY budget-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY shared/ /app/shared/
COPY budget-service/ /app/budget-service/

ENV PYTHONPATH=/app

EXPOSE 8003

CMD ["uvicorn", "budget-service.main:app", "--host", "0.0.0.0", "--port", "8003"]