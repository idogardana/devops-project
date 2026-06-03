# Stage 1 - build & test
FROM python:3.11-slim AS builder
WORKDIR /app
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ .
RUN pytest test_app.py

# Stage 2 - production image
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /app .
RUN pip install --no-cache-dir flask
EXPOSE 5000
CMD ["python", "app.py"]