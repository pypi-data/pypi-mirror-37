# -*- coding: utf-8 -*-
import getopt
import mimetypes
import os
import posixpath
import sys
import urllib

from flask import Flask
from flask import render_template, request
from flask import send_from_directory

from fserver.conf import CDN_JS
from fserver.conf import GetArg
from fserver.conf import VIDEO_SUFFIX
from fserver.util import debug

app = Flask(__name__, template_folder='templates')

if sys.version_info < (3, 4):
    reload(sys)
    sys.setdefaultencoding("gbk")


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def do_get(path):
    debug('get_ls: ', path, [a for a in request.args.values()])
    arg = GetArg(request.args)
    local_path = translate_path(path)

    if os.path.isdir(local_path):  # 目录
        return list_dir(path)
    elif os.path.exists(local_path):  # 非目录
        if arg.mode is None or arg.mode == GetArg.MODE_NORMAL:
            if get_suffix(path) in VIDEO_SUFFIX:
                return play_video(path)
            else:
                return respond_file(path)
        elif arg.mode == GetArg.MODE_TXT:
            return respond_file(path, mime='text/plain')
        elif arg.mode == GetArg.MODE_DOWN:
            return respond_file(path, as_attachment=True)
        elif arg.mode == GetArg.MODE_VIDEO:
            return play_video(path)

    return render_template('error.html', error='No such dir or file: ' + path)


def list_dir(path):
    debug('list_dir', path)
    local_path = translate_path(path)
    arg = GetArg(request.args)
    if os.path.isdir(local_path):  # 目录
        lst = os.listdir(local_path)
        for i, l in enumerate(lst):
            if os.path.isdir('/'.join([local_path, l])):
                lst[i] += '/'
        return render_template('list.html',
                               path=path,
                               arg=arg.format_for_url(),
                               list=lst)


def respond_file(path, mime=None, as_attachment=False):
    debug('respond_file:', path)
    if os.path.isdir(path):
        return do_get(path)
    local_path = translate_path(path)
    if mime is None or mime not in mimetypes.types_map.values():  # mime 无效
        mime = mimetypes.guess_type(local_path)[0]
        if mime is None:  # 无法获取类型，默认使用 text/plain
            mime = 'text/plain'

    return send_from_directory(get_parent_path(local_path),
                               get_filename(local_path),
                               mimetype=mime,
                               as_attachment=as_attachment)


def play_video(path):
    debug('play_video:', path)
    if os.path.isdir(translate_path(path)):
        return do_get(path)

    arg = GetArg(request.args)
    suffix = get_suffix(path)
    t = suffix if arg.play is None else arg.play

    try:
        tj = CDN_JS[t]
        tjs = []
    except Exception as e:
        debug(e)
        tj = ''
        tjs = CDN_JS.values()
    return render_template('video.html',
                           name=get_filename(path),
                           url='/%s?%s=%s' % (path, GetArg.ARG_MODE, GetArg.MODE_DOWN),
                           type=t,
                           typejs=tj,
                           typejss=tjs)


def get_filename(path):
    try:
        return path[path.rindex('/') + 1:]
    except Exception as e:
        debug(e)
        try:
            return path[path.rindex('\\') + 1:]
        except Exception as e2:
            debug(e2)
            return path


def get_parent_path(path):
    try:
        filename = get_filename(path)
        return path[:path.rindex(filename)]
    except Exception as e:
        debug(e)
        return ''


def get_suffix(path):
    try:
        return path[path.rindex('.') + 1:]
    except Exception as e:
        debug(e)
        return ''


def translate_path(path):
    """Translate a /-separated PATH to the local filename syntax.

    Components that mean special things to the local file system
    (e.g. drive or directory names) are ignored.  (XXX They should
    probably be diagnosed.)

    """
    # abandon query parameters
    path = path.split('?', 1)[0]
    path = path.split('#', 1)[0]
    # Don't forget explicit trailing slash when normalizing. Issue17324
    trailing_slash = path.rstrip().endswith('/')
    try:
        path = urllib.parse.unquote(path, errors='surrogatepass')
    except Exception:
        path = urllib.unquote(path)
    path = posixpath.normpath(path)
    words = path.split('/')
    words = filter(None, words)
    path = os.getcwd()
    for word in words:
        if os.path.dirname(word) or word in (os.curdir, os.pardir):
            # Ignore components that are not a simple file/directory name
            continue
        path = os.path.join(path, word)
    if trailing_slash:
        path += '/'
    return path


def main():
    port = 2000
    help_str = '''usage: python fserver_app.py [-h] [port]

  positional arguments:
    port                  Specify alternate port [default: 2000]

  optional arguments:
    -h, --help            show this help message and exit

  arguments of url:
    m                     get_arg to set the mode of processing method of file
                          Such as http://localhost:port?m=dv to download the file specified by url
                          value 'p' to play file with Dplayer
                          value 'v' to show the file specified by url
                          value 'dv' to download the file specified by url
 '''

    try:
        options, args = getopt.getopt(sys.argv[1:], "h", ["help"])
    except getopt.GetoptError as e:
        print('error:', e.msg)
        print(help_str)
        sys.exit()

    if len(args) > 0:
        port = args[0]
        if not port.isdigit():
            print('error: port must be int, input:', port)
            sys.exit()

    for name, value in options:
        if name in ['-h', '--help']:
            print(help_str)
            sys.exit()

    app.run(
        host='0.0.0.0',
        port=port,
    )


if __name__ == '__main__':
    main()
