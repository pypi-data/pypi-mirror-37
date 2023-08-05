# -*- coding: utf-8 -*-
import getopt
import sys

from gevent.pywsgi import WSGIServer

from fserver import conf
from fserver import util
from fserver.fserver_app import app as application

help_str_short = 'usage: fserver [-h] [-d] [--ip ADDRESS] [port]'
help_str = '''
Uasge:
  fserver [-h] [-d] [--ip ADDRESS] [port]

Positional arguments:
  port                  Specify alternate port [default: 2000]

Optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           use debug mode of fserver
  -i ADDRESS, --ip ADDRESS,
                        Specify alternate bind address [default: all interfaces]

 '''


def run_fserver():
    try:
        options, args = getopt.getopt(sys.argv[1:], 'hdvi:', ['help', 'debug', 'version', 'ip='])
    except getopt.GetoptError as e:
        print(help_str_short)
        print('error:', e.msg)
        sys.exit()

    # init conf
    ip = '0.0.0.0'
    port = 2000
    conf.DEBUG = False

    if len(args) > 0:
        port = args[0]
        if not port.isdigit():
            print('error: port must be int, input:', port)
            sys.exit()

    for name, value in options:
        if name in ['-h', '--help']:
            print(help_str)
            sys.exit()
        if name in ['-d', '--debug']:
            conf.DEBUG = True
        if name in ['-i', '--ip']:
            ip = value
        if name in ['-v', '--version']:
            print('fserver', conf.VERSION, 'build at', conf.BUILD_TIME)
            print('Python', sys.version)
            sys.exit()

    print('fserver is available at following address:')
    if ip == '0.0.0.0':
        ips = util.get_ip_v4()
        for _ip in ips:
            print('  %s:%s' % (_ip, port))
    else:
        print('  %s:%s' % (ip, port))

    http_server = WSGIServer((ip, int(port)), application)
    http_server.serve_forever()


if __name__ == '__main__':
    run_fserver()
