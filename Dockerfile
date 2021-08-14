FROM python:3.7-alpine 
# the image our docker-file will be build upon. This is a light-weight python image.
# you can find images here: https://hub.docker.com/

LABEL maintainer="MoellerAI"

ENV PYTHONUNBUFFERED 1
# turns the environment to run python in a buffered mode. This is often preferred.

COPY ./requirements.txt /requirements.txt
# copy our requirements file to the docker image.
RUN pip install -r /requirements.txt
# run our requirements using pip.

RUN mkdir /app