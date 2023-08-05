# -*- coding: utf-8 -*-
import fserver


def debug(*args):
    if fserver.conf.DEBUG:
        for i in args:
            print i,
        print
