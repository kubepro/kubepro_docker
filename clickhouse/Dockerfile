FROM ubuntu:18.04

ARG repository="deb http://repo.yandex.ru/clickhouse/deb/stable/ main/"
ARG version=\*

RUN apt-get update \
    && apt-get install -y apt-transport-https dirmngr python python-pip bash less \
    && pip install yattag \
    && mkdir -p /etc/apt/sources.list.d \
    && apt-key adv --keyserver keyserver.ubuntu.com --recv E0C56BD4 \
    && echo $repository | tee /etc/apt/sources.list.d/clickhouse.list \
    && apt-get update \
    && env DEBIAN_FRONTEND=noninteractive apt-get install --allow-unauthenticated -y clickhouse-server=$version clickhouse-common-static=$version libgcc-7-dev \
    && rm -rf /var/lib/apt/lists/* /var/cache/debconf \
    && apt-get clean

COPY clickhouse_gen_config.py /clickhouse_gen_config.py
COPY clickhouse_gen_users.py /clickhouse_gen_users.py
COPY clickhouse_flush_dns.sh /clickhouse_flush_dns.sh

EXPOSE 9000 8123 9009
VOLUME /var/lib/clickhouse
