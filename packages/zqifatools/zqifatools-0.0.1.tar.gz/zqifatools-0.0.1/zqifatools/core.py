# coding:utf-8

import random


# 工具类
class Tools(object):

    # 随机数字
    @staticmethod
    def ran_num(arg=None):
        # 生成六位的数值不在传入的列表中
        num = random.randint(100000, 999999)
        if arg and num in arg:
            return random_num(arg)
        return num

    # 随机字符串
    @staticmethod
    def ran_str(len=None, max_len=None):
        try:
            if len and len >= 1:
                if max_len and max_len > len:
                    len = random.randint(len, max_len)
                return ''.join(random.sample(string.ascii_letters, 1)
                               + random.sample(string.ascii_letters + string.digits, len - 1))
        except Exception:
            pass
        return ''
