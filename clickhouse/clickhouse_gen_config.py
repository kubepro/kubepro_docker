#!/usr/bin/env python

import subprocess
import shlex
import os
import re
import sys

from yattag import Doc, indent

HOSTNAME = subprocess.check_output(shlex.split('hostname -s')).strip()
if not re.match(r'(.*)-([0-9]+)$', HOSTNAME):
    print('Hostname does not match the pattern "name-ordinal"')
    sys.exit(1)
NAME = HOSTNAME.split('-')[0]
ORDINAL = int(HOSTNAME.split('-')[1])
DOMAIN = subprocess.check_output(shlex.split('hostname -d')).strip()

# we expect this value to be even
CH_REPLICAS = int(os.environ['CH_REPLICAS'])
CH_SERVERS = ["{}-{}.{}".format(NAME, i, DOMAIN) for i in range(CH_REPLICAS)]
CH_ZOOKEEPER_SERVERS = [
    zk.split(':') for zk in os.environ['CH_ZOOKEEPER_SERVERS'].split(',')
]
CH_USERS_XML = os.environ['CH_USERS_XML']
CH_USER = os.environ['CH_USER']
CH_PASSWORD = os.environ['CH_PASSWORD']

doc, tag, text = Doc().tagtext()

doc.asis('<?xml version="1.0"?>')
with tag('yandex'):
    with tag('logger'):
        with tag('level'):
            text('trace')
        with tag('log'):
            text('/var/lib/clickhouse/clickhouse.log')
        with tag('errorlog'):
            text('/var/lib/clickhouse/clickhouse.err.log')
        with tag('size'):
            text('1000M')
        with tag('count'):
            text('10')
    with tag('http_port'):
        text('8123')
    with tag('tcp_port'):
        text('9000')

    with tag('interserver_http_port'):
        text('9009')
    with tag('interserver_http_host'):
        text('.'.join([HOSTNAME, DOMAIN]))
    with tag('listen_host'):
        text('::')
    with tag('max_connections'):
        text('4096')
    with tag('keep_alive_timeout'):
        text('3')
    with tag('max_concurrent_queries'):
        text('100')
    with tag('path'):
        text('/var/lib/clickhouse')
    with tag('tmp_path'):
        text('/var/lib/clickhouse/tmp')

    with tag('mark_cache_size'):
        text('5368709120')
    with tag('uncompressed_cache_size'):
        text('8589934592')

    with tag('max_insert_block_size'):
        text('4194304')

    with tag('merge_tree'):
        with tag('parts_to_delay_insert'):
            text('300')
        with tag('parts_to_throw_insert'):
            text('600')
        with tag('max_delay_to_insert'):
            text('2')

    with tag('default_profile'):
        text('default')
    with tag('users_config'):
        text(CH_USERS_XML)
    with tag('default_database'):
        text('default')

    with tag('remote_servers'):
        with tag('cluster'):
            for i in range(CH_REPLICAS / 2):
                with tag('shard'):
                    with tag('replica'):
                        with tag('host'):
                            text(CH_SERVERS[2 * i])
                        with tag('port'):
                            text('9000')
                        with tag('user'):
                            text(CH_USER)
                        with tag('password'):
                            text(CH_PASSWORD)
                    with tag('replica'):
                        with tag('host'):
                            text(CH_SERVERS[2 * i + 1])
                        with tag('port'):
                            text('9000')
                        with tag('user'):
                            text(CH_USER)
                        with tag('password'):
                            text(CH_PASSWORD)

    with tag('zookeeper'):
        for i, zk in enumerate(CH_ZOOKEEPER_SERVERS):
            with tag('node', index=i+1):
                with tag('host'):
                    text(zk[0])
                with tag('port'):
                    text(zk[1])

    with tag('macros'):
        with tag('shard'):
            text(ORDINAL / 2)
        with tag('replica'):
            text(HOSTNAME)

print(indent(doc.getvalue()))
