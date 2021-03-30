#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re, sys, os, traceback, signal


def singleton_decorator(cls, *args, **kwargs):
    """定义一个单例装饰器"""
    instance = {}

    def wrapper_singleton(*args, **kwargs):
        if cls not in instance:
            instance[cls] = cls(*args, **kwargs)
        return instance[cls]
    return wrapper_singleton


@singleton_decorator
class MyBeautifulGirl(object):
    """使用单例装饰器修饰一个类"""

    def __init__(self, name):
        self.__name = name
        print("遇见" + name + "，我一见钟情！ ")

    def show_my_heart(self):
        print(self.__name + "就是我心中的唯一！")


def on_signal_int(signum, frame):
    print("\nReceive SIGINT[Ctrl+C] to stop process by force !")
    sys.exit(-1)


def register_signal():
    signal.signal(signal.SIGINT, on_signal_int)


def main():
    register_signal()

    jenny = MyBeautifulGirl("Jenny")
    jenny.show_my_heart()
    kimi = MyBeautifulGirl("Kimi")
    kimi.show_my_heart()
    print("id(jenny):", id(jenny), " id(kimi):", id(kimi))

    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
        sys.exit(2)
