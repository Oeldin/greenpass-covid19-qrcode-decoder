# syntax=docker/dockerfile:1

FROM python:3.10-buster as build

WORKDIR /gdec
RUN apt update && apt install -y libzbar-dev

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000
ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:8000", "-w", "2", "--access-logfile", "-", "app:app"]
