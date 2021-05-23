FROM python:3-buster

##
## Install OS Dependencies
##

RUN apt-get update && apt-get install -y \
  libpwiz-tools \
  imagemagick \
  && rm -rf /var/lib/apt/lists/*

##
## Install App
##

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /usr/src/app
COPY kitten.* /tmp/

EXPOSE 8080

ENTRYPOINT ["python3"]

CMD ["-m", "openapi_server"]
