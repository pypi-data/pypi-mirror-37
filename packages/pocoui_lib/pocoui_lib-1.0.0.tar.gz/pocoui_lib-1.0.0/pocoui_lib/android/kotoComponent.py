#!/usr/bin/env python
# -*- coding: utf-8 -*-
from poco.exceptions import PocoNoSuchNodeException
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco()
from pocoui_lib.android import kotoList
from pocoui_lib.android import kotoPage
import random
# 处理一般的pickerView
def picker_swipe():
    poco('android.widget.NumberPicker').wait(timeout=6)
    if poco('android.widget.NumberPicker').exists():
        poco('android.widget.NumberPicker').swipe('up')
        print(poco(text="完成").exists())
        if poco(text="完成").exists():
            poco(text="完成").click()
        else:
            print('完成 note existes'.encode(encoding='utf-8'))

# 选项数组随机点击，单选
def random_item_click(array):
    index = random.randint(0, len(array)-1)
    item = array[index]
    print('================%d' % (index))
    # print("click the point", item)
    poco(text=item).wait(timeout=10)
    if(poco(text=item).exists()):
        poco(text=item).click(sleep_interval=6.0)
    else:
        print(('%s not exists' % (item)).encode(encoding='utf-8'))
        pass
    return item
# 点击之后延长秒
def polong_click(pocoPoint,time=6.0):
    # print("click the point", item)
    if(pocoPoint.exists()):
        pocoPoint.click(sleep_interval=time)
    else:
        print('point not exists')
        pass


