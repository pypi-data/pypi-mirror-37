from pyfi import WindHelper as w, line_graph, double_lines
import matplotlib.pyplot as plt
"""
performace
indicator
"""
maxdd = lambda eqd: (eqd.cumsum().expanding().max() - eqd.cumsum()).max()


def m_sharpe(eqd, bk=0.0):
    """monthly sharpe ratio"""
    try:
        if eqd.sum() == 0:
            return -100
        return ((eqd.mean() - bk / 12) / eqd.std()) * (12 ** 0.5)
    except BaseException as e:
        print(e)


def excess_msp(eqd, base_eqd, bk=0.0):
    return m_sharpe(eqd, bk) - m_sharpe(base_eqd, bk)


def monthly_backtest(score, pattern=1):
    """
    分值为发布时间点,也就是建仓点,基于净价指数进行择时
    :param score:
    :param pattern: 1: [0,1,2]; 5: [0,0.2,0.4,0.6,0.8,1,1.2,1.4,1.6,1.8,2.0]
    :return:
    """
    begin_date = score.index[0]
    end_date = score.index[-1]
    ytm = w.edb(codes=["gz10y"], begin_date=begin_date, end_date=end_date).iloc[:, 0]
    bond_ind = w.wsd(code="CBA01552.CS", begin_date=begin_date, end_date=end_date, paras=["close"]).iloc[:, 0].resample(
        "M").last()  # 1结尾为财富值， 2结尾为净价
    #    bond_ind = W.edb(["M0265833"], begin_date, end_date).iloc[:,0].resample("M").last()
    if pattern == 5:
        pos = score.apply(lambda x: 1 + (1.0 / pattern) * x).shift(1)
    elif pattern == 1:
        pos = score.apply(lambda x: 0 if x < 0 else (1 if x == 0 else 2)).shift(1)
    elif pattern == -1:
        pos = score.apply(lambda x: -1 if x < 0 else (0 if x == 0 else 1)).shift(1)
    else:
        raise Exception("The pattern is invalid, man ~~ please reset it, OK??? Only 1 and 5 is permitted")
    d_bond_ind = bond_ind.pct_change().dropna()
    benchmark = (1 + d_bond_ind).cumprod()
    # pos_ = WindHelper.monthly_data_with_td(pos)
    port = (pos * d_bond_ind + 1).cumprod().dropna()
    alpha = port - benchmark
    # draw the graph
    fig = plt.figure(figsize=(10, 15))
    ax1 = plt.subplot(311)
    double_lines(series1=score, series2=ytm, title="ytm V.S. score",
                 lgd1="score", lgd2="10y ytm", ax=ax1, fig=fig)
    ax2 = plt.subplot(312)
    ax3 = ax2.twinx()
    line_graph([port, benchmark], legend_list=["port", "benchmark"],
               title="curve battle", ax=ax2, fig=fig)
    ax3.fill_between(alpha.index, 0, alpha.values, color="grey", alpha=0.3)
    ax4 = plt.subplot(313)
    line_graph([pos], legend_list=["position"],
               title="Check the position change frequencey", ax=ax4, fig=fig)
    plt.suptitle("Monthly backtest with clean index", fontsize=36)
    plt.show()
    d_port = port.pct_change().dropna()
    d_bench = benchmark.pct_change().dropna()
    return {"score": score,
            "port": port,
            "pos": pos,
            "benchmark": benchmark,
            "alpha": alpha,
            "ytm": ytm.resample("M").last(),
            "report": {
                "最大回撤": maxdd(d_port),
                "夏普比率": m_sharpe(d_port),
                "超额夏普比率": excess_msp(d_port, d_bench),
                "年均alpha": alpha[-1]/((len(port)-1)/12),
                "年均alpha": alpha[-1]/((len(port)-1)/12),
                "calmar": port[-1]**(1/(len(port)-1)*12)-1
            }
            }


def monthly_backtest_with_repo(score, pattern=1):
    """
    分值为发布时间点,也就是建仓点
    """
    b_weight = 1
    import matplotlib.pyplot as plt
    begin_date = score.index[0]
    end_date = score.index[-1]
    if pattern == 5:
        pos = score.apply(lambda x: b_weight + (b_weight / pattern) * x).shift(1)
    elif pattern == 1:
        pos = score.apply(lambda x: 0 if x < 0 else (b_weight if x == 0 else 2*b_weight)).shift(1)
    else:
        raise Exception("The pattern is invalid, man ~~ please reset it, OK??? Only 1 and 5 is permitted")
    ytm = w.edb(codes=["gz10y"], begin_date=begin_date, end_date=end_date).iloc[:, 0]
    r007 = w.edb(codes=["M0041653"], begin_date=begin_date, end_date=end_date).iloc[:, 0].resample("M").last()
    bond_ind = w.wsd("CBA01551.CS", ["close"], begin_date, end_date).iloc[:, 0] \
        .resample("M").last()  # 1结尾为财富值， 2结尾为净价
    d_bond_ind = bond_ind.pct_change().dropna()
    money_ind = (r007 / 100 / 12 + 1).cumprod()
    d_money_ind = money_ind.pct_change().dropna()
    # establish the benchmark
    benchmark = (d_bond_ind * b_weight + (d_money_ind * (1 - b_weight)) + 1).cumprod()
    # pos_ = WindHelper.monthly_data_with_td(pos)
    port = (pos * d_bond_ind + (1 - pos) * d_money_ind + 1).cumprod().dropna()
    alpha = port - benchmark
    # draw the picture
    fig = plt.figure(figsize=(10, 15))
    ax1 = plt.subplot(311)
    double_lines(series1=score, series2=ytm, title="ytm V.S. score",
                 lgd1="score", lgd2="10y ytm", ax=ax1, fig=fig)
    ax2 = plt.subplot(312)
    ax3 = ax2.twinx()
    line_graph([port, benchmark], legend_list=["port", "benchmark"],
               title="curve battle", ax=ax2, fig=fig)
    ax3.fill_between(alpha.index, 0, alpha.values, color="grey", alpha=0.3)
    ax4 = plt.subplot(313)
    line_graph([pos], legend_list=["position"],
               title="Check the position change frequencey", ax=ax4, fig=fig)
    plt.suptitle("Monthly Backtest with wealth index", fontsize=36)
    plt.show()
    d_port = port.pct_change().dropna()
    d_bench = benchmark.pct_change().dropna()
    return {"score": score,
            "port": port,
            "pos": pos,
            "benchmark": benchmark,
            "alpha": alpha,
            "ytm": ytm.resample("M").last(),
            "report": {
                "最大回撤": maxdd(d_port),
                "夏普比率": m_sharpe(d_port),
                "超额夏普比率": excess_msp(d_port, d_bench),
                "年均alpha": alpha[-1]/((len(port)-1)/12),
                "calmar": port[-1]**(1/(len(port)-1)*12)-1
            }
            }


def monthly_backtest_with_repo2(score, pattern=1):
    """
    保持仓位始终不变，防止前期的alpha对后期的alpha带来增益的影响
    分值为发布时间点,也就是建仓点
    
    """
    b_weight = 1
    import matplotlib.pyplot as plt
    begin_date = score.index[0]
    end_date = score.index[-1]
    if pattern == 5:
        pos = score.apply(lambda x: b_weight + (b_weight / pattern) * x).shift(1)
    elif pattern == 1:
        pos = score.apply(lambda x: 0 if x < 0 else (1 if x == 0 else 2)).shift(1)
    else:
        raise Exception("The pattern is invalid, man ~~ please reset it, OK??? Only 1 and 5 is permitted")
    ytm = w.edb(codes=["gz10y"], begin_date=begin_date, end_date=end_date).iloc[:, 0]
    r007 = w.edb(codes=["M0041653"], begin_date=begin_date, end_date=end_date).iloc[:, 0].resample("M").last()
    bond_ind = w.wsd("CBA01551.CS", ["close"], begin_date, end_date).iloc[:, 0] \
        .resample("M").last()  # 1结尾为财富值， 2结尾为净价
    d_bond_ind = bond_ind.pct_change().dropna()
    money_ind = (r007 / 100 / 12 + 1).cumprod()
    d_money_ind = money_ind.pct_change().dropna()
    # establish the benchmark
    benchmark = 1 + (d_bond_ind * b_weight + (d_money_ind * (1 - b_weight))).cumsum()
    # pos_ = WindHelper.monthly_data_with_td(pos)
    port = 1 + (pos * d_bond_ind + (1 - pos) * d_money_ind).cumsum().dropna()
    alpha = port - benchmark
    # draw the picture
    fig = plt.figure(figsize=(10, 15))
    ax1 = plt.subplot(311)
    double_lines(series1=score, series2=ytm, title="ytm V.S. score",
                 lgd1="score", lgd2="10y ytm", ax=ax1, fig=fig)
    ax2 = plt.subplot(312)
    ax3 = ax2.twinx()
    line_graph([port, benchmark], legend_list=["port", "benchmark"],
               title="curve battle", ax=ax2, fig=fig)
    ax3.fill_between(alpha.index, 0, alpha.values, color="grey", alpha=0.3)
    ax4 = plt.subplot(313)
    line_graph([pos], legend_list=["position"],
               title="Check the position change frequencey", ax=ax4, fig=fig)
    plt.suptitle("Monthly Backtest with wealth index(No cum)", fontsize=36)
    plt.show()
    return {"score": score,
            "port": port,
            "pos": pos,
            "benchmark": benchmark,
            "alpha": alpha,
            "ytm": ytm.resample("M").last()
            }


def monthly_backtest_with_extrem(score, pattern=1):
    pass


def daily_backtest(score, pattern=1):
    pass
