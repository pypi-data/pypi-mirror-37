#/usr/bin/env python
# -*- coding: UTF-8 -*-

from poco.drivers.ios import iosPoco
poco = iosPoco()

def back():
    if (poco("返回").exists()):
        poco("返回").click()
