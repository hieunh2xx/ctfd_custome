# Bước 1: Tạo chroot cho ứng dụng web
FROM python:3.9-slim as web-chroot

# Tạo người dùng cho ứng dụng
RUN /usr/sbin/useradd -u 1000 user

# Set the working directory in the container
WORKDIR /usr/src/web-app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Bước 2: Tạo Docker image chính cho ứng dụng
FROM gcr.io/kctf-docker/challenge@sha256:0f7d757bcda470c3bbc063606335b915e03795d72ba1d8fdb6f0f9ff3757364f

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -yq --no-install-recommends tzdata python3 python3-pip mysql-client mysql-server \
    && ln -fs /usr/share/zoneinfo/Europe/Berlin /etc/localtime \
    && dpkg-reconfigure --frontend noninteractive tzdata \
    && rm -rf /var/lib/apt/lists/*

# Sao chép ứng dụng web vào image chính
COPY --from=web-chroot /usr/src/web-app /web-app

# Tạo thư mục cho dữ liệu MySQL và thiết lập quyền
RUN mkdir -p /var/lib/mysql /var/run/mysqld && \
    chown -R mysql:mysql /var/lib/mysql /var/run/mysqld

# Tạo cơ sở dữ liệu
# It's better to use a separate script to initialize MySQL
COPY init_db.sql /tmp/init_db.sql

RUN service mysql start && \
    mysql < /tmp/init_db.sql

RUN pip install --no-cache-dir -r /web-app/requirements.txt

EXPOSE 5000

# CMD để khởi động cả ứng dụng web và dịch vụ cơ sở dữ liệu
# CMD service mysql start && python3 /web-app/app.py
CMD (kctf_drop_privs nsjail --config /web-app/web-servers.nsjail.cfg --port 5000 -- python3 /web-app/app.py  )
