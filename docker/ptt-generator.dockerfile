FROM python:3.9-slim-buster
LABEL authors="water92001@gmail.com"
ENV PYTHONIOENCODING UTF-8

# Install requirements and prerequisite
RUN apt-get update \
    && apt-get install -y --assume-yes --no-install-recommends build-essential

# Install gtk+ for GUI develpment
#RUN apt-get install -y libgtk-3-dev

# clean cached
RUN rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip

# copy require
COPY ./requirements.txt ./

# Install required packages
RUN pip install \
    --no-cache-dir \
    --requirement ./requirements.txt

RUN mkdir -p /ptt-generator
COPY ./src /ptt-generator/src

ENV PYTHONPATH="$PYTHONPATH:/ptt-generator/src"
WORKDIR /ptt-generator

#EXPOSE 8080
#CMD /husky-generation/run.sh
