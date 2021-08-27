FROM python:3.7-alpine 
# the image our docker-file will be build upon. This is a light-weight minimum python image.
# you can find images here: https://hub.docker.com/

LABEL maintainer="MoellerAI"

ENV PYTHONUNBUFFERED 1
# turns the environment to run python in a buffered mode. This is often preferred.

COPY ./requirements.txt /requirements.txt
# copy our requirements file to the docker image.

RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
        gcc libc-dev linux-headers postgresql-dev
# making sure postgres can be installed

RUN pip install -r /requirements.txt
# run our requirements using pip.
RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app
# creates an empty folder on our docker-image called /app.
# then it switches to that folder as its default directory.
# everything we will run from our docker-container will start from the /app folder unless else specified.
# the last thing we do is to copy the folder from our local machine to the docker-image.

RUN adduser -D user
USER user
# we create a temporary user which can use the docker container instead of using the root. 
# switch to the new user. This is due to security purposes.



# THIS DOCKERFILE CAN BE RUN USING "docker build ."