# Dockerfile
FROM python:3.9.10-alpine3.14
WORKDIR /srv
RUN pip install --upgrade pip
RUN pip install flask
RUN pip install flask-cors
RUN pip install couchdb
COPY ./api.py /srv
ENV FLASK_APP=api
ENTRYPOINT ./wait-for-it.sh couchserver:5984 FLASK_APP=api flask run --host=0.0.0.0