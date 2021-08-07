FROM python:3.9.6-slim-buster

WORKDIR /opt/working

ENV PORT=$PORT

COPY . .
RUN pip install -r requirements.txt

CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000}"]