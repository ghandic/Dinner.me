FROM python:3.9

WORKDIR /opt/working

COPY . .
RUN pip install -r requirements.txt

CMD [ "python", "app.py" ]