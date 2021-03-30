#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re, sys, os, traceback, signal
# 引入 ABCMeta 和 abstractmethod 来定义抽象类和抽象方法
from abc import ABCMeta, abstractmethod


class Context(metaclass=ABCMeta):
    """状态模式的上下文环境类"""
    def __init__(self):
        self.__states = []
        self.__cur_state = None
        # 状态发生变化依赖的属性, 当这一变量由多个变量共同决定时可以将其单独定义成一个类
        self.__state_info = 0

    def add_state(self, state):
        if state not in self.__states:
            self.__states.append(state)

    def change_state(self, state):
        if state is None:
            return False

        if self.__cur_state is None:
            print("O =>", state.get_name())
        else:
            print(self.__cur_state.get_name(), "=>", state.get_name())
        self.__cur_state = state
        self.add_state(state)
        return True

    def get_state(self):
        return self.__cur_state

    def _set_state_info(self, state_info):
        self.__state_info = state_info

        for state in self.__states:
            if state.is_match(state_info):
                self.change_state(state)

    def get_state_info(self):
        return self.__state_info


class State:
    """状态的基类"""

    def __init__(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    def is_match(self, state_info):
        """状态的属性 stateInfo 是否在当前的状态范围内"""
        return False

    @abstractmethod
    def behavior(self, context):
        pass


# 单例的装饰器
def singleton(cls, *args, **kwargs):
    """构造一个单例的装饰器"""
    instance = {}

    def __singleton(*args, **kwargs):
        if cls not in instance:
            instance[cls] = cls(*args, **kwargs)
        return instance[cls]
    return __singleton


@singleton
class SolidState(State):
    """固态"""
    def __init__(self, name):
        super().__init__(name)

    def is_match(self, state_info):
        return state_info < 0

    def behavior(self, context):
        print("我性格高冷，当前体温", context.get_state_info(),
              "℃，我坚如钢铁，仿如一冷血动物，请用我砸人，嘿嘿......")


@singleton
class LiquidState(State):
    """液态"""
    def __init__(self, name):
        super().__init__(name)

    def is_match(self, state_info):
        return 0 <= state_info < 100

    def behavior(self, context):
        print("我性格温和，当前体温", context.get_state_info(),
              "℃，我可滋润万物，饮用我可让你活力倍增......")


@singleton
class GaseousState(State):
    """气态"""
    def __init__(self, name):
        super().__init__(name)

    def is_match(self, state_info):
        return state_info >= 100

    def behavior(self, context):
        print("我性格热烈，当前体温", context.get_state_info(),
              "℃，飞向天空是我毕生的梦想，在这你将看不到我的存在，我将达到无我的境界......")


class Water(Context):
    """水(H2O)"""
    def __init__(self):
        super().__init__()
        self.add_state(SolidState("固态"))
        self.add_state(LiquidState("液态"))
        self.add_state(GaseousState("气态"))
        self.set_temperature(25)

    def get_temperature(self):
        return self.get_state_info()

    def set_temperature(self, temperature):
        self._set_state_info(temperature)

    def rise_temperature(self, step):
        self.set_temperature(self.get_temperature() + step)

    def reduce_temperature(self, step):
        self.set_temperature(self.get_temperature() - step)

    def behavior(self):
        state = self.get_state()
        if isinstance(state, State):
            state.behavior(self)


def on_signal_int(signum, frame):
    print("\nReceive SIGINT[Ctrl+C] to stop process by force !")
    sys.exit(-1)


def register_signal():
    signal.signal(signal.SIGINT, on_signal_int)


def main():
    register_signal()

    # 常温水（25℃）
    water = Water()
    water.behavior()

    # 冰水（-4℃）
    water.set_temperature(-4)
    water.behavior()

    # 水温加热+18℃ = 14℃
    water.rise_temperature(18)
    water.behavior()

    # 水温继续加热+110℃ = 124℃
    water.rise_temperature(110)
    water.behavior()

    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
        sys.exit(2)
