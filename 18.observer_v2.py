#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re, sys, os, traceback, signal
# 引入 ABCMeta 和 abstractmethod 来定义抽象类和抽象方法
from abc import ABCMeta, abstractmethod


class Observer(metaclass=ABCMeta):
    """观察者的基类"""
    @abstractmethod
    def update(self, observable, obj):
        pass


class Observable:
    """被观察者的基类"""
    def __init__(self):
        self.__observers = []

    def add_observer(self, observer):
        self.__observers.append(observer)

    def remove_observer(self, observer):
        self.__observers.remove(observer)

    def notify_observers(self):
        for o in self.__observers:
            o.update(self)


class WaterHeater(Observable):
    """热水器：战胜寒冬的有利武器"""
    def __init__(self):
        super().__init__()
        self.__temperature = 25

    def get_temperature(self):
        return self.__temperature

    def set_temperature(self, temperature):
        self.__temperature = temperature
        print("当前温度是： " + str(self.__temperature) + "℃")
        self.notify_observers()


class WashingMode(Observer):
    """该模式用于洗澡"""
    def update(self, observable):
        if isinstance(observable, WaterHeater) and 50 <= observable.get_temperature() < 70:
            print("水已烧好！温度正好，可以用来洗澡了。 ")


class DrinkingMode(Observer):
    """该模式用于饮用"""
    def update(self, observable):
        if isinstance(observable, WaterHeater) and observable.get_temperature() >= 100:
            print("水已烧开！可以用来饮用了。 ")


def on_signal_int(signum, frame):
    print("\nReceive SIGINT[Ctrl+C] to stop process by force !")
    sys.exit(-1)


def register_signal():
    signal.signal(signal.SIGINT, on_signal_int)


def main():
    register_signal()

    # 热水器
    heater = WaterHeater()

    # 观察者，观察热水器
    washing_observer = WashingMode()
    drinking_observer = DrinkingMode()
    heater.add_observer(washing_observer)
    heater.add_observer(drinking_observer)

    # 热水器温度变化
    heater.set_temperature(40)
    heater.set_temperature(60)
    heater.set_temperature(100)

    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
        sys.exit(2)
