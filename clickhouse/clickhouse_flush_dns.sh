#!/usr/bin/env bash

set -x

while true; do
    sleep ${CH_FLUSH_DNS_INTERVAL}
    clickhouse client --user ${CH_USER} --password ${CH_PASSWORD} --host $(hostname -f) -q 'SYSTEM DROP DNS CACHE'
done
