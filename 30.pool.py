#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re, sys, os, traceback, signal
# 引入 ABCMeta 和 abstractmethod 来定义抽象类和抽象方法
from abc import ABCMeta, abstractmethod
import logging
import time
logging.basicConfig(level=logging.INFO)


class PooledObject:
    """池对象,也称池化对象"""
    def __init__(self, obj):
        self.__obj = obj
        self.__busy = False

    def get_object(self):
        return self.__obj

    def set_object(self, obj):
        self.__obj = obj

    def is_busy(self):
        return self.__busy

    def set_busy(self, busy):
        self.__busy = busy


class ObjectPool(metaclass=ABCMeta):
    """对象池"""

    # 对象池初始化大小
    InitialNumOfObjects = 10
    # 对象池最大的大小
    MaxNumOfObjects = 50

    def __init__(self):
        self.__pools = []
        for i in range(0, ObjectPool.InitialNumOfObjects):
            obj = self.create_pooled_object()
            self.__pools.append(obj)

    @abstractmethod
    def create_pooled_object(self):
        """创建池对象, 由子类实现该方法"""
        pass

    def borrow_object(self):
        """借用对象"""
        # 如果找到空闲对象，直接返回
        obj = self._find_free_object()
        if (obj is not None):
            logging.info("%x 对象已被借用, time:%s", id(obj),
                         time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
            return obj
        # 如果对象池未满，则添加新的对象
        if len(self.__pools) < ObjectPool.MaxNumOfObjects:
            pooledObj = self.add_object()
            if pooledObj is not None:
                pooledObj.setBusy(True)
                logging.info("%x 对象已被借用, time:%s", id(obj),
                         time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
                return pooledObj.getObject()
        # 对象池已满且没有空闲对象，则返回 None
        return None

    def return_object(self, obj):
        """归还对象"""

        for pooled_obj in self.__pools:
            if pooled_obj.get_object() == obj:
                pooled_obj.set_busy(False)
                logging.info("%x 对象已归还, time:%s", id(obj),
                             time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
                break

    def add_object(self):
        """添加新对象"""

        obj = None
        if len(self.__pools) < ObjectPool.MaxNumOfObjects:
            obj = self.create_pooled_object()
            self.__pools.append(obj)
            logging.info("添加新对象%x, time:", id(obj),
                         time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
        return obj

    def clear(self):
        """清空对象池"""
        self.__pools.clear()

    def _find_free_object(self):
        """查找空闲的对象"""
        obj = None
        for pooled_obj in self.__pools:
            if not pooled_obj.is_busy():
                obj = pooled_obj.get_object()
                pooled_obj.set_busy(True)
                break
        return obj


class PowerBank:
    """移动电源"""
    def __init__(self, serial_num, electric_quantity):
        self.__serialNum = serial_num
        self.__electricQuantity = electric_quantity
        self.__user = ""

    def get_serial_num(self):
        return self.__serialNum

    def get_electric_quantity(self):
        return self.__electricQuantity

    def set_user(self, user):
        self.__user = user

    def get_user(self):
        return self.__user

    def show_info(self):
        print("序列号:%03d 电量:%d%% 使用者:%s" % (self.__serialNum,
                                           self.__electricQuantity, self.__user))


class PowerBankPool(ObjectPool):
    """存放移动电源的智能箱盒"""
    __serial_num = 0

    @classmethod
    def get_serial_num(cls):
        cls.__serial_num += 1
        return cls.__serial_num

    def create_pooled_object(self):
        power_bank = PowerBank(PowerBankPool.get_serial_num(), 100)
        return PooledObject(power_bank)


def on_signal_int(signum, frame):
    print("\nReceive SIGINT[Ctrl+C] to stop process by force !")
    sys.exit(-1)


def register_signal():
    signal.signal(signal.SIGINT, on_signal_int)


def main():
    register_signal()

    # 创建充电宝池
    power_bank_pool = PowerBankPool()

    # 租借第一个充电宝
    power_bank1 = power_bank_pool.borrow_object()
    if power_bank1 is not None:
        power_bank1.set_user("Tony")
    power_bank1.show_info()

    # 租借第二个充电宝
    power_bank2 = power_bank_pool.borrow_object()
    if power_bank2 is not None:
        power_bank2.set_user("Sam")
    power_bank2.show_info()

    # 归还第一个充电宝
    power_bank_pool.return_object(power_bank1)

    # 租借第三个充电宝，应该是刚才还掉的那个
    power_bank3 = power_bank_pool.borrow_object()
    if power_bank3 is not None:
        power_bank3.set_user("Aimee")
    power_bank3.show_info()

    # 归还所有充电宝
    power_bank_pool.return_object(power_bank2)
    power_bank_pool.return_object(power_bank3)

    power_bank_pool.clear()

    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
        sys.exit(2)
