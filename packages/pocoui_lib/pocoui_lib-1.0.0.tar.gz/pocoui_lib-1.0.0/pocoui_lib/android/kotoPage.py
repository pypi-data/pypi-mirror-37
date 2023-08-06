#/usr/bin/env python
# -*- coding: UTF-8 -*-
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco()

from pocoui_lib.android import kotoList


# 适用单选列表
def random_item():
    # 等待列表渲染完成
    kotoList.random_item()

def is_page(name):
    return poco(text=name).exists()
