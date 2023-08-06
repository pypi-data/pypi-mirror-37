# -*- coding: utf-8 -*-
import getopt
import sys

from gevent.pywsgi import WSGIServer

from fserver import conf
from fserver import util
from fserver.fserver_app import app as application

help_str_short = 'usage: fserver [-h] [-d] [-u] [-o] [-u] [-o] [-i ADDRESS] [port]'
help_str = '''
Usage:
  fserver [-h] [-d] [-u] [-o] [-i ADDRESS] [port]

Positional arguments:
  port                  Specify alternate port [default: 2000]

Optional arguments:
  -d, --debug           Use debug mode of fserver
  -h, --help            Show this help message and exit
  -i ADDRESS, --ip ADDRESS,
                        Specify alternate bind address [default: all interfaces]
  -o, --override        Set upload file with override mode, only valid when [-u] is used
  -u, --upload          Open upload file function. This function is closed by default

 '''


def run_fserver():
    try:
        options, args = getopt.getopt(sys.argv[1:], 'hdvi:uo',
                                      ['help', 'debug', 'version', 'ip=', 'upload', 'override'])
    except getopt.GetoptError as e:
        print(help_str_short)
        print('error: %s' % e.msg)
        sys.exit()

    # init conf
    ip = '0.0.0.0'
    port = 2000

    if len(args) > 0:
        port = args[0]
        if not port.isdigit():
            print('error: port must be int, input: %s' % port)
            sys.exit()

    for name, value in options:
        if name in ['-h', '--help']:
            print(help_str)
            sys.exit()
        if name in ['-d', '--debug']:
            conf.DEBUG = True
            continue
        if name in ['-i', '--ip']:
            ip = value
            continue
        if name in ['-u', '--upload']:
            conf.UPLOAD = True
            continue
        if name in ['-o', '--override']:
            conf.UPLOAD_OVERRIDE_MODE = True
            continue
        if name in ['-v', '--version']:
            print('fserver %s build at %s' % (conf.VERSION, conf.BUILD_TIME))
            print('Python %s' % sys.version)
            sys.exit()

    print('fserver is available at following address:')
    if ip == '0.0.0.0':
        ips = util.get_ip_v4()
        for _ip in ips:
            print('  http://%s:%s' % (_ip, port))
    else:
        print('  %s:%s' % (ip, port))

    http_server = WSGIServer((ip, int(port)), application)
    http_server.serve_forever()


if __name__ == '__main__':
    run_fserver()
