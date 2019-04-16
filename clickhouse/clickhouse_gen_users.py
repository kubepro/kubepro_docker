#!/usr/bin/env python

import subprocess
import shlex
import os
import re
import sys

from yattag import Doc, indent

CH_USER = os.environ['CH_USER']
CH_PASSWORD = os.environ['CH_PASSWORD']

doc, tag, text = Doc().tagtext()

doc.asis('<?xml version="1.0"?>')
with tag('yandex'):
    with tag('users'):
        with tag(CH_USER):
            with tag('password'):
                text(CH_PASSWORD)
            with tag('networks'):
                with tag('ip'):
                    text('::/0')
            with tag('profile'):
                text('default')
            with tag('quota'):
                text('default')
    with tag('profiles'):
        with tag('default'):
            with tag('max_threads'):
                text('8')
    with tag('quotas'):
        with tag('default'):
            with tag('interval'):
                with tag('duration'):
                    text('3600')
                with tag('queries'):
                    text('0')
                with tag('errors'):
                    text('0')
                with tag('result_rows'):
                    text('0')
                with tag('read_rows'):
                    text('0')
                with tag('execution_time'):
                    text('0')

print(indent(doc.getvalue()))
