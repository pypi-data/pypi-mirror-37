#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil
from ubersicht.coffee import Coffee

WIDGETS = "%s/Library/Application Support/Übersicht/widgets" % os.environ["HOME"]


class Widget(Coffee):
    name = None

    @property
    def path(self):
        return os.path.join(WIDGETS, "%s" % self.name)

    def create(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        index = os.path.join(self.path, "index.coffee")
        open(index, "w").write(self.coffee())
        return self

    def rm(self):
        if os.path.exists(self.path):
            shutil.rmtree(self.path)
        return self

    def __str__(self):
        return '<Widget "%s">' % self.path


def _widgets():
    for l in os.listdir(WIDGETS):
        path = os.path.join(WIDGETS, l)
        if os.path.splitext(path)[1] == ".widget" and os.path.isdir(path):
            yield path


def widgets():
    return list(_widgets())
