#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re, sys, os, traceback, signal


class Tony(object):
    """程序员Tony"""
    __instance = None
    __isFirstInit = False

    def __new__(cls, name):
        if not cls.__instance:
            Tony.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, name):
        if not self.__isFirstInit:
            self.__my_girl = name
            Tony.__isFirstInit = True

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
    tony_24 = Tony("Jenny")
    tony_24.meet("Jenny")
    tony_24.show_my_heart()

    # 26岁的Tony
    tony_26 = Tony("Kimi")
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
