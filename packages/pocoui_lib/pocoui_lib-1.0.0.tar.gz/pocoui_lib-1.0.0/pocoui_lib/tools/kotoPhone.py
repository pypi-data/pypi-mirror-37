#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import string
# 获取手机号码
def get_phone_number():
    pre_lst = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150", "151", "152", "153", "155", "156", "157", "158", "159", "186", "187",
"188"]
    return random.choice(pre_lst) + ''.join(random.sample(string.digits, 8))
# 添加微信
def get_weixin():
    return "".join(random.sample(string.ascii_letters, 8))
#
def get_num():
    return "".join(random.sample(string.digits,2))
if __name__ == "__main__":
    get_phone_number()
