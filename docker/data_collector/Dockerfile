FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y git curl gnupg apt-transport-https ca-certificates && \
    curl -s https://dl.k6.io/key.gpg | gpg --dearmor -o /etc/apt/trusted.gpg.d/k6.gpg && \
    echo "deb https://dl.k6.io/deb stable main" > /etc/apt/sources.list.d/k6.list && \
    apt-get update && \
    apt-get install -y k6 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app .

RUN chmod +x ../../k6/run_tests.sh || true

EXPOSE 8000

CMD ["python", "data_collector.py"]