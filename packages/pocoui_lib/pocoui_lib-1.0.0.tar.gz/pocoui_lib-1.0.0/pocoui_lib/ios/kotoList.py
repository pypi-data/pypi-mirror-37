#/usr/bin/env python
# -*- coding: UTF-8 -*-

from poco.drivers.ios import iosPoco
poco = iosPoco()
import random
from poco.exceptions import *

# 适用单选列表
def random_item(tablePoco):
    # 等待列表渲染完成
    table = tablePoco
    table.wait(timeout=5)
    firstnode = poco("Table").child("Cell")[0]
    firstnode.wait(timeout=5)

    # 随机点击
    itemlist = poco("Table").child("Cell")
    # 可能会造成 Click position out of screen
    count = len(list(itemlist))

    if count > 2:
        end = count - 2
    else:
        end = count - 1
    index = random.randint(0, end)

    try:
        itemlist[index].click()
    except PocoNoSuchNodeException:
        print('list not exit item[%d]' % (index))

# 找到scrollview上的元素，滑倒底部元素
def scroll_to(nodeName, lastnodeName="保存"):
    n = poco(nodeName)
    while not n:
        try:
            poco("Table").scroll(direction='vertical', percent=0.6, duration=1.0)
        except PocoNoSuchNodeException:
            print(('scroll not exit %s' % (nodeName)).encode(encoding='utf-8'))

        # 滑倒最底部
        if poco(lastnodeName):
            break

    return n
