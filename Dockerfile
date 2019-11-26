FROM python:3.6-slim-buster

MAINTAINER Freshons

ADD . /code
WORKDIR /code

RUN pip install -r requirements.txt

CMD ["gunicorn", "-c", "gunicorn_config.py", "entry:app"]
