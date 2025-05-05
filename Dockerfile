FROM python:3.8.14-slim-buster

WORKDIR /code

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

ENV TZ="Asia/Ho_Chi_Minh"
ENV DEBIAN_FRONTEND noninteractive
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

COPY ./requirements.txt /code/requirements.txt
RUN pip install --upgrade -r /code/requirements.txt

COPY . /code

ENTRYPOINT ["python", "app.py"]