from pyfi import WindHelper as w, double_lines, line_graph
import matplotlib.pyplot as plt


def template1():
    pass


def template2():
    pass


templates = {
    "历史上牛市回调的持续时间": template1,
    "股市与债市相对配置价值比较": template2,
}

template_names = templates.keys()


def ytm_compare(data, title="10y ytm V.S. data", lgd="data"):
    begin_date = data.index[0]
    end_date = data.index[-1]
    ytm = w.edb(codes=["gz10y"], begin_date=begin_date, end_date=end_date).iloc[:, 0]
    fig = plt.figure(figsize=(16, 9))
    ax1 = plt.subplot(111)
    double_lines(series1=data, series2=ytm, title=title,
                 lgd1=lgd, lgd2="10y Treasury YTM", ax=ax1, fig=fig)
    plt.show()
