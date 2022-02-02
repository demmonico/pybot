FROM python:3

COPY ./docker/requirements.txt /
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app

ENTRYPOINT ["python", "main.py"]
