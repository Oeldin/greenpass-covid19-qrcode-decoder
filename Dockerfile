# syntax=docker/dockerfile:1

FROM python:3.10-buster as build
ARG MAIN_DIR=/gdec

WORKDIR $MAIN_DIR
COPY requirements.txt requirements.txt

RUN python -m venv ./venv
RUN pip install -r requirements.txt

FROM python:3.10-alpine

WORKDIR $MAIN_DIR

RUN python -m venv ./venv

COPY . .
COPY --from=build ./venv .

ENTRYPOINT ["python", "-m", "flask", "run"]
