# -*- coding: utf-8 -*-
from __future__ import print_function

import os

from fserver import conf


def debug(*args):
    if conf.DEBUG:
        min_len = 40
        msg = ''
        for i in args:
            msg += str(i) + ' '
        msg = '| ' + msg.replace('\n', '\n| ')
        ln = max([len(i) + 3 for i in msg.split('\n')])
        ln = ln if ln > min_len else min_len
        print('_' * ln)
        print(msg)
        print('=' * ln)


def _get_ip_v4_ipconfig():
    ips = []
    try:
        ip_cmd = os.popen('ipconfig 2>&1').read().split('\n')
        [ips.append(s[s.index(':') + 2:]) for s in ip_cmd if 'ipv4' in s.lower()]
        if '127.0.0.1' not in ips:
            ips.append('127.0.0.1')
    except Exception as e:
        debug(e.message)
    return ips


def _get_ip_v4_ifconfig():
    ips = []
    sh = r"""ifconfig 2>&1 | \
    awk -F '[ :]' 'BEGIN{print "succeed"}/inet /{ for (i=1;i<=NF;i++){ if ($i~/[0-9]\./) {print $i;break }} }' 2>&1 """
    try:
        ip_cmd = os.popen(sh).read()
        if 'succeed' in ip_cmd:
            ips.extend([i for i in ip_cmd.split('\n') if i != '' and i != 'succeed'])
        if '127.0.0.1' not in ips:
            ips.append('127.0.0.1')
    except Exception as e:
        debug(e.message)
    return ips


def _get_ip_v4_ip_add():
    ips = []
    sh = r"""ip -4 add 2>&1 |awk 'BEGIN{print "succeed"} $2 ~/^[0-9]+\./ {print $2}' | awk -F/ '{print $1}'"""
    try:
        ip_cmd = os.popen(sh).read()
        if 'succeed' in ip_cmd:
            ips.extend([i[:i.index('/')] for i in ip_cmd.split('\n') if i != '' and i != 'succeed'])
        if '127.0.0.1' not in ips:
            ips.append('127.0.0.1')
    except Exception as e:
        debug(e)
    return ips


def get_ip_v4():
    ips = []
    if os.name == 'nt':
        ips = _get_ip_v4_ipconfig()
    elif os.name == 'posix':
        ips = _get_ip_v4_ip_add()
        if len(ips) == 0 or ips is None:
            ips = _get_ip_v4_ifconfig()

    for ip in [i for i in ips]:
        if ip.startswith('169.254.'):
            ips.remove(ip)

    return ips


if __name__ == '__main__':
    print(_get_ip_v4_ipconfig())
    print(_get_ip_v4_ip_add())
    print(_get_ip_v4_ifconfig())
