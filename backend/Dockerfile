FROM python:3.9.6-slim-buster

WORKDIR /opt/working

ARG MONGO_USERNAME
ARG MONGO_PASSWORD

ENV PORT=$PORT
ENV MONGO_USERNAME=$MONGO_USERNAME
ENV MONGO_PASSWORD=$MONGO_PASSWORD

COPY . .
RUN pip install -r requirements.txt

CMD ["sh", "-c", "uvicorn api:api --host 0.0.0.0 --port ${PORT:-8000}"]