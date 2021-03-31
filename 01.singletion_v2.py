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
class Tony(object):
    """使用单例装饰器修饰一个类"""

    def __init__(self):
        self.__my_girl = "Jenny"

    def meet(self, name):
        if name == self.__my_girl:
            print("遇见" + name + "，我一见钟情！")
        else:
            print("遇见" + name + "，我置若罔闻！")

    def show_my_heart(self):
        print(self.__my_girl + "就是我心中的唯一！")


def on_signal_int(signum, frame):
    print("\nReceive SIGINT[Ctrl+C] to stop process by force !")
    sys.exit(-1)


def register_signal():
    signal.signal(signal.SIGINT, on_signal_int)


def main():
    register_signal()

    # 24岁的Tony
    tony_24 = Tony()
    tony_24.meet("Jenny")
    tony_24.show_my_heart()

    # 26岁的Tony
    tony_26 = Tony()
    tony_26.meet("Kimi")
    tony_26.show_my_heart()

    print("id(tony_24):", id(tony_24), " id(tony_26):", id(tony_26))

    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
        sys.exit(2)
