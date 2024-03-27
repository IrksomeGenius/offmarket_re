FROM python:3.8-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy scripts into container directory
COPY ./dags/. /app 

ENTRYPOINT ["python"]