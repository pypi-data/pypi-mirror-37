# 和processing 模块有点重叠
from datetime import timedelta, datetime
import scipy.optimize as optimize
import pandas as pd
import numpy as np
import time


def exeTime(func):
    def newFunc(*args, **args2):
        t0 = time.time()
        print("@%s, {%s} start" % (time.strftime("%X", time.localtime()), func.__name__))
        back = func(*args, **args2)
        print("@%s, {%s} end" % (time.strftime("%X", time.localtime()), func.__name__))
        print("@%.3fs taken for {%s}" % (time.time() - t0, func.__name__))
        return back

    return newFunc


def nearest(items, pivot):
    """
    the reusult will be a little smaller than pivot with the positive timedelta
    :param items: the samples
    :param pivot: the target
    :return:
    """
    return min(items, key=lambda x: abs((x + timedelta(1) - pivot)))


def get_end_date():
    """确定开始时间，计算最新的已经结算的交易日"""
    from pyfi import WindHelper
    # 确定结束时间
    # 结束时间为该合约的最后交易日和当前日期的最小值
    last_trade_date = WindHelper.t_days_offset(offset=0, cur_date=datetime.now())
    # 确定结束时间
    if datetime.now().hour >= 19:  # 以晚上19点为界限
        end_date = last_trade_date
    elif datetime.now().date() > last_trade_date.date():  # 当天不是交易日
        end_date = last_trade_date
    else:  # 既非节假日，且当然的数据也没有生成
        end_date = WindHelper.t_days_offset(offset=-1, cur_date=datetime.now())  # datetime类型
    return end_date


def get_date_list(begin_date, end_date):
    # begin_date, end_date是形如‘20160601’的字符串或datetime格式
    date_l = [x for x in list(pd.date_range(start=begin_date, end=end_date))]
    return date_l


# 常用债券计算函数
def get_ytm_by_net(net, maturity, cupn, freq, par=100, guess=3):
    """
    根据净价, 待偿期限，票息，付息次数，面值计算债券的到期收益率
    :param net:
    :param par:
    :param maturity:
    :param cupn:
    :param freq:
    :param guess:
    :return:
    """

    yearsToNxCupn = maturity - 1. / freq * np.floor(freq * maturity)
    cupnCount = int(np.ceil(freq * maturity))
    coupon = cupn / 100. * par / freq
    if yearsToNxCupn == 0.:
        dt = [(i + 1.) / freq for i in range(cupnCount)]
    else:
        dt = [yearsToNxCupn + i / freq for i in range(cupnCount)]
    ytm_func = lambda y: sum([coupon / (1. + y / 100. / freq) ** (freq * t) for t in dt]) + \
                         par / (1. + y / 100. / freq) ** (freq * maturity) - (
                                 1. / freq - yearsToNxCupn) * cupn - net
    return optimize.newton(ytm_func, guess)


def get_dirty(ytm, maturity, cupn, freq, par=100.):
    """
    based on ytm, maturity, coupon and frequency to calculate the dirty price
    :param ytm:
    :param par:
    :param maturity:
    :param cupn: 3.65 instead of 0.0365
    :param freq:
    :return:
    """
    yearsToNxCupn = maturity - 1.0 / freq * np.floor(freq * maturity)
    cupnCount = int(np.ceil(freq * maturity))
    coupon = cupn / 100. * par / freq
    if yearsToNxCupn == 0:
        dt = [(i + 1.) / freq for i in range(cupnCount)]
    else:
        dt = [yearsToNxCupn + i / freq for i in range(cupnCount)]
    return sum([coupon / (1. + ytm / 100. / freq) ** (freq * t) for t in dt]) + \
        par / (1. + ytm / 100. / freq) ** (freq * maturity)


def get_net(ytm, par, maturity, cupn, freq):
    daysToNxCupn = maturity - 1.0 / freq * np.floor(freq * maturity)
    dirty = get_dirty(ytm, maturity, cupn, freq, par)
    return dirty - (1. / freq - daysToNxCupn) * cupn


def get_years_to_nxcupn(maturity, freq):
    """
    calculate the period to next coupon marked by year unit
    :param maturity:
    :param freq:
    :return:
    """
    yearsToNxCupn = maturity - 1.0 / freq * np.floor(freq * maturity)
    return yearsToNxCupn
