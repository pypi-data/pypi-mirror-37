import matplotlib.pyplot as plt
import matplotlib as mpl


def init():
    """
    一些初始化设置，主要是为了显示负号和中文
    :return:
    """
    mpl.rcParams["axes.unicode_minus"] = False
    plt.rcParams["font.sans-serif"] = ["SimHei"]
    plt.rcParams["axes.unicode_minus"] = False


def line_graph(series, title="multi lines graph", legend_list="", fig=None, ax=None, save=False):
    """df_list的时间轴得一样
    :param series:
    :param title:
    :param legend_list:
    :param fig: 
    :param ax:
    """
    init()
    if fig is None:
        fig = plt.figure(figsize=(16, 6))
    if ax is None:
        ax = plt.subplot(111)
    ax.set_title(title, fontsize=18)
    ax.grid(axis="both", linestyle='--')
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(True)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(True)
    ax.tick_params(axis='both', labelsize=16)
    # ax_list = [{}] * len(series_list)
    for i in range(len(series)):
        ax.plot(series[i].index.values, series[i].values, lw=2., linestyle="-")
        for tick in ax.get_xticklabels():
            tick.set_rotation(30)
    ax.legend(legend_list, fontsize=16, loc=0)
    if save:
        fig.savefig(title + ".jpg")


def double_lines(series1,
                 series2,
                 lgd1="series1",
                 lgd2="series2",
                 title="double axis graph",
                 colors=["grey", "red"],
                 figname="",
                 fig=None,
                 ax=None):
    """快速画出双线对比图
    :param series1:
    :param series2:
    :param lgd1:
    :param lgd2:
    :param title:
    :param colors:
    :param figname:
    :param fig:
    :param ax:
    """
    init()
    if fig is None:
        fig = plt.figure(figsize=(16, 9))
    if ax is None:
        ax1 = plt.subplot(111)
    else:
        ax1 = ax
    ax1.set_title(title, fontsize=18)
    ax1.grid(axis="both", linestyle='--')
    ax1.spines["top"].set_visible(False)
    ax1.spines["bottom"].set_visible(True)
    ax1.spines["right"].set_visible(False)
    ax1.spines["left"].set_visible(True)
    ax1.tick_params(axis='both', labelsize=16)
    if type(series1) is not list:
        ax1.plot(series1.index.values, series1.values, color=colors[0])
        ax1.legend([lgd1], fontsize=16, loc=1)
    else:
        for i in range(len(series1)):
            ax1.plot(series1[i].index.values, series1[i].values, lw=2., linestyle="-")
            ax1.legend(lgd1, fontsize=16, loc=1)
    ax2 = ax1.twinx()
    if type(series2) is not list:
        ax2.plot(series2.index.values, series2.values, color=colors[1])
        ax2.legend([lgd2], fontsize=16, loc=2)
    else:
        for i in range(len(series2)):
            ax2.plot(series2[i].index.values, series2[i].values, lw=2., linestyle="-")
            ax2.legend(lgd2, fontsize=16, loc=2)
    ax2.tick_params(axis='both', labelsize=16)
    if figname is not "":
        fig.savefig(figname)
    # plt.show()
