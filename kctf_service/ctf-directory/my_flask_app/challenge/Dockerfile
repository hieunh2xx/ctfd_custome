FROM gcr.io/kctf-docker/challenge@sha256:0f7d757bcda470c3bbc063606335b915e03795d72ba1d8fdb6f0f9ff3757364f

COPY web-servers.nsjail.cfg /home/user/web-servers.nsjail.cfg

COPY web-apps /web-apps

RUN ln -s /chroot/web-apps /web-apps

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -yq --no-install-recommends tzdata python3 python3-pip mysql-client mysql-server \
    && ln -fs /usr/share/zoneinfo/Europe/Berlin /etc/localtime \
    && dpkg-reconfigure --frontend noninteractive tzdata \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r /web-apps/requirements.txt

EXPOSE 1337

#CMD service mysql start && mysql < /web-apps/init_db.sql && python3 /web-apps/app.py

#CMD để khởi động cả ứng dụng web và dịch vụ cơ sở dữ liệu
CMD kctf_setup \
    && (kctf_drop_privs nsjail --config /home/user/web-servers.nsjail.cfg --port 1337 -- /bin/bash -c "service mysql start && mysql < /web-apps/init_db.sql && python3 /web-apps/app.py")
