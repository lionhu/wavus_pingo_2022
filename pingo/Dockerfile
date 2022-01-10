FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1


RUN mkdir -p /usr/src/app

# Adding mandatory packages to docker
RUN apk update && apk add --no-cache \
    postgresql postgresql-client\
    zlib \
    jpeg \
    openblas \
    libstdc++

# Installing temporary packages required for installing requirements.pip
RUN apk add --no-cache --virtual build-deps \
     py3-pip py3-pip py3-pip py3-brotli \
    gcc musl-dev python3-dev pango\
    postgresql-dev\
    zlib-dev \
    jpeg-dev \
    g++ \
    openblas-dev \
    cmake \
    openssl-dev cargo libjpeg \
    libffi-dev libc-dev gettext \
    && ln -s /usr/include/locale.h /usr/include/xlocale.h

# Update pip
RUN pip install --upgrade pip

# Installing scipy
#RUN pip3 install --no-cache-dir --disable-pip-version-check scipy==1.3.1

# Installing numpy, scipy, psycopg2, gensim
RUN pip3 install --no-cache-dir \
    numpy \
    pandas \
    psycopg2
#    scipy
#    gensim==3.8.1 # remove it if not necessary

# Installing requirements.pip from project
COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt
#RUN pip install django-pandas
#RUN pip install py3dns==3.2.1

# update apk repo
RUN echo "http://dl-4.alpinelinux.org/alpine/v3.14/main" >> /etc/apk/repositories && \
    echo "http://dl-4.alpinelinux.org/alpine/v3.14/community" >> /etc/apk/repositories

# install chromedriver
#RUN apk update
RUN apk add chromium chromium-chromedriver

# removing temporary packages from docker and removing cache
RUN apk del build-deps && \
    find -type d -name __pycache__ -prune -exec rm -rf {} \; && \
    rm -rf ~/.cache/pip

COPY . /usr/src/app/
COPY fonts/. /usr/share/fonts
WORKDIR /usr/src/app
