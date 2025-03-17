FROM python:3.11-alpine AS dependencies

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && rm requirements.txt


FROM python:3.11-alpine AS build

WORKDIR /app
COPY --from=dependencies /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

COPY app.py .
COPY templates ./templates
COPY static ./static


FROM build AS prod

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=192.168.100.143
ENV FLASK_RUN_PORT=8080
ENV REDIS_HOST=redis


CMD ["sh", "-c", "python -m flask run --host=$FLASK_RUN_HOST --port=$FLASK_RUN_PORT"]

