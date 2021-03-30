#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re, sys, os, traceback, signal


class MyBeautifulGirl(object):
    """我的漂亮女神"""
    __instance = None
    __isFirstInit = False

    def __new__(cls, name):
        if not cls.__instance:
            MyBeautifulGirl.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, name):
        if not self.__isFirstInit:
            self.__name = name
            print("遇见" + name + "，我一见钟情！")
            MyBeautifulGirl.__isFirstInit = True
        else:
            print("遇见" + name + "，我置若罔闻！")

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
