#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from public import public


@public
def kill():
    _pid = pid()
    if _pid:
        os.system("kill -9 %s &> /dev/null" % _pid)


@public
def pid():
    for l in os.popen("ps -ax").read().splitlines():
        if "Übersicht.app/Contents/MacOS/Übersicht" in l:
            return int(list(filter(None, l.split(" ")))[0])


@public
def start():
    if not pid():
        return os.system("open -a Übersicht")


@public
def restart():
    kill()
    start()
