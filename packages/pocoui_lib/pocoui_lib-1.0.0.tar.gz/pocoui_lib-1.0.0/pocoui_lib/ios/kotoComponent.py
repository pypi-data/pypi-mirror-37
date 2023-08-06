#/usr/bin/env python
# -*- coding: UTF-8 -*-

from poco.drivers.ios import iosPoco
poco = iosPoco()
import random
from poco.exceptions import *
from pocoui_lib.ios import kotoList
from pocoui_lib.ios import kotoPage

# 相册选择
def photo_picker():
    itemlist = poco("CollectionView").child("Cell")
    # 可能会造成 Click position out of screen
    count = len(list(itemlist))
    end = count - 1
    index = random.randint(0, end)

    try:
        itemlist[index].child("Button").click()
    except PocoNoSuchNodeException:
        print('list not exit item[%d]' % (index))

    if (poco("完成").exists()):
        poco("完成").click()

# 品牌车系二级联动，三级联动
def choose_brand():
    while kotoPage.is_page("选择品牌"):
        table = poco("Window").poco("Table")[0]
        kotoList.random_item(table)


# 处理一般的pickerView
def picker_swipe():
    if (poco("Picker").exists()):
        for wheel in poco("Picker").child("PickerWheel"):
            wheel.swipe('up')

    if (poco("完成").exists()):
        poco("完成").click()



# 选项数组随机点击，单选
def random_item_click(array):
    item = random.choice(array)
    poco(item).click()
    return item
