FROM gcr.io/kctf-docker/challenge@sha256:0f7d757bcda470c3bbc063606335b915e03795d72ba1d8fdb6f0f9ff3757364f

# Copy Flask app and requirements
COPY . .

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -yq --no-install-recommends python3.8-venv tzdata python3 python3-pip mysql-client mysql-server \
    && ln -fs /usr/share/zoneinfo/Europe/Berlin /etc/localtime \
    && dpkg-reconfigure --frontend noninteractive tzdata \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install -r requirements.txt

# Set up MySQL
RUN service mysql start && \
    mysql -u root < init_db.sql

# Copy nsjail config
COPY web-servers.nsjail.cfg /etc/nsjail.cfg

# Command to run nsjail and flask
CMD kctf_setup && \
    kctf_drop_privs nsjail --config /etc/nsjail.cfg --port 1337 -- /bin/bash -c "python3 app.py"
