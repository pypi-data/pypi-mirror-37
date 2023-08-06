#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import string
import time
from poco.exceptions import PocoNoSuchNodeException
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco()
# recyclerview随机点击
def random_item():
    # 等待列表渲染完成
    table = poco(type='android.support.v7.widget.RecyclerView')
    table.wait(timeout=10)
    itemlist =table.child()
    firstnode = itemlist[0]
    firstnode.wait(timeout=10)
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
        print('list not exist item[%d]' % (index))
# 找到scrollview 并滑动到底部
def scroll_to(nodeName, percents, lastNodeName):
    scrollView = poco(type='ScrollView')
    if not scrollView.exists():
         scrollView = poco(type='android.widget.FrameLayout')
    n = poco(text=nodeName)
    lastNode = poco(text=lastNodeName)
    if scrollView.exists():
        while not n:
            try:
                if(percents>0):
                    scrollView.scroll(direction='vertical', percent=percents, duration=1.0)
                else:
                    scrollView.scroll(direction='vertical', percent=percents, duration=1.0)
            except PocoNoSuchNodeException:
                print('scroll not exist %s ' % (nodeName))
        # 滑倒最底部poco("com.souche.fengche:id/scrollView_custom")
            if lastNode.exists():
                break
        if not n.exists():
            print((' %s not exists' % (nodeName)).encode(encoding='utf-8'))
    else:
        print((' %s not exists' % (nodeName)).encode(encoding='utf-8'))
    time.sleep(5)
    return n
# recyclerview 传poco(id)
def random_poco_point_item(pocoPoint):
    # 等待列表渲染完成
    table = pocoPoint
    table.wait(timeout=10)
    itemlist =table.child()
    firstnode = itemlist[0]
    firstnode.wait(timeout=10)
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
        print('list not exist item[%d]' % (index))