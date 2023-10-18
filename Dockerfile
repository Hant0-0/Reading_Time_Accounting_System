FROM python:3.10-alpine3.17

COPY requirements.txt /temp/requirements.txt
COPY time_reading /time_reading
WORKDIR /time_reading
EXPOSE 8000

RUN pip install -r /temp/requirements.txt

RUN adduser --disabled-password time_reading-user

USER time_reading-user