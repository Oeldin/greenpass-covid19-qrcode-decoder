# syntax=docker/dockerfile:1

ARG MAIN_DIR=/gdec

FROM python:3.10-buster as build
ARG MAIN_DIR

WORKDIR $MAIN_DIR
COPY requirements.txt requirements.txt

#ENV VIRTUAL_ENV=$MAIN_DIR/venv
#RUN python -m venv $VIRTUAL_ENV
#ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install wheel
RUN pip install -r requirements.txt

#FROM python:3.10-alpine
#ARG MAIN_DIR

RUN apt update && apt install -y libzbar-dev
#RUN apk update && apk add libzbar gcc  && \
#  ln -s /usr/lib/libzbar.so.0 /usr/lib/libzbar.so

#WORKDIR $MAIN_DIR
#ENV VIRTUAL_ENV=$MAIN_DIR/venv
ENV PRODUCTION=True

COPY . .
#COPY --from=build $MAIN_DIR/venv ./venv
#ENV PATH="$VIRTUAL_ENV/bin:$PATH"

EXPOSE 5000:3659
#ENTRYPOINT ["python"]
ENTRYPOINT ["gunicorn", "app:app"]
#ENTRYPOINT ["python", "-m", "pip", "list"]
#ENTRYPOINT ["ls", "/usr/lib"]
#ENTRYPOINT echo $LD_LIBRARY_PATH

