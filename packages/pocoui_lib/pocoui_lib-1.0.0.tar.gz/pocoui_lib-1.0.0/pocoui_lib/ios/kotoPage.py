#/usr/bin/env python
# -*- coding: UTF-8 -*-

from poco.drivers.ios import iosPoco
poco = iosPoco()
import random
from poco.exceptions import *
from pocoui_lib.ios import kotoList

# 适用单选列表
def random_item():
    # 等待列表渲染完成
    table = poco("Table")
    kotoList.random_item(table)


def is_page(name):
    return poco(label=name).exists()
