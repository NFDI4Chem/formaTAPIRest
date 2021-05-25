FROM python:3-buster

##
## Install OS Dependencies
##

RUN curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - \
  && apt-get update && apt-get install -y \
  apt-transport-https \
  libpwiz-tools \
  imagemagick

RUN echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" > /etc/apt/sources.list.d/kubernetes.list \
  kubectl \
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
