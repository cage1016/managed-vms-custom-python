FROM google/python

RUN apt-get update && apt-get install -y -q --no-install-recommends

WORKDIR /app
RUN virtualenv /env

ADD requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN /env/bin/pip install -r requirements.txt

# Adds the rest of the application source
ADD . /app

ENTRYPOINT ["/env/bin/python", "/app/main.py"]