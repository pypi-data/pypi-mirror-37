# -*- coding: utf-8 -*-

VERSION = '0.0.10'
BUILD_TIME = '2018/10/25'

DEBUG = False

UPLOAD_OVERRIDE_MODE = False
UPLOAD = False

VIDEO_SUFFIX = ['mp4', 'flv', 'hls', 'dash']
CDN_JS = {
    'flv': '/static/flv.min.js',
    'hls': '/static/hls.js@latest',
    'dash': '/static/dash.all.min.js',
    'mp4': ''
}
