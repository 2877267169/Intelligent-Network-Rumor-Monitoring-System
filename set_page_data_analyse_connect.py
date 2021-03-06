from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import os, sys

import MainWindow
from data import transform_json_to_txt
from data import bert_train_complex
import running_state
import json
from analysis import analysis_processer
# matplotlib 和qt链接的包
# 修复打包的问题
import matplotlib

from main_window_run import my_app_img_dir

matplotlib.use("Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

# 画图对象
import set_page_corpus_connect

my_page_data_analyse_attitude_tend_graph_fig = plt.figure()
my_page_data_analyse_attitude_pie_graph_fig = plt.figure()
my_page_data_analyse_intensity_tend_graph_fig = plt.figure()
my_page_data_analyse_intensity_pie_graph_fig = plt.figure()
# 利用对象构建组件
my_page_data_analyse_attitude_tend_graph_FC = FigureCanvas(my_page_data_analyse_attitude_tend_graph_fig)
my_page_data_analyse_attitude_pie_graph_FC = FigureCanvas(my_page_data_analyse_attitude_pie_graph_fig)
my_page_data_analyse_intensity_tend_graph_FC = FigureCanvas(my_page_data_analyse_intensity_tend_graph_fig)
my_page_data_analyse_intensity_pie_graph_FC = FigureCanvas(my_page_data_analyse_intensity_pie_graph_fig)
# 真正画图的东西
my_page_data_analyse_attitude_tend_graph_ax = my_page_data_analyse_attitude_tend_graph_fig.add_subplot(1, 1, 1)
my_page_data_analyse_attitude_pie_graph_ax = my_page_data_analyse_attitude_pie_graph_fig.add_subplot(1, 1, 1)
my_page_data_analyse_intensity_tend_graph_ax = my_page_data_analyse_intensity_tend_graph_fig.add_subplot(1, 1, 1)
my_page_data_analyse_intensity_pie_graph_ax = my_page_data_analyse_intensity_pie_graph_fig.add_subplot(1, 1, 1)

my_ui = MainWindow.Ui_MainWindow()


def set_page_data_analyse_connect(ui: MainWindow.Ui_MainWindow):
    global my_ui
    my_ui = ui

    # 信号与槽的链接
    ui.my_page_data_analyse_commandLinkButton_start.clicked.connect(start_analyse)
    ui.my_page_data_analyse_load_commandLinkButton.clicked.connect(load)
    ui.my_page_data_analyse_doubleSpinBox.valueChanged.connect(write_threshold)
    ui.my_page_data_analyse_set_default_pushButton.clicked.connect(set_default)
    ui.my_page_data_analyse_save_pushButton.clicked.connect(my_save)
    analysis_processer.analise_message.s_send_analyse_process_bar.connect(set_ana_process_bar)
    analysis_processer.analise_message.s_send_analyse_process_text.connect(set_process_text)
    analysis_processer.analise_message.s_send_analyse_start_draw.connect(ana_start_draw)

    # 加入组件的操作
    ui.my_page_data_analyse_attitude_tend_graph.layout().addWidget(my_page_data_analyse_attitude_tend_graph_FC)
    ui.my_page_data_analyse_attitude_pie_graph.addWidget(my_page_data_analyse_attitude_pie_graph_FC)
    ui.my_page_data_analyse_intensity_tend_graph.addWidget(my_page_data_analyse_intensity_tend_graph_FC)
    ui.my_page_data_analyse_intensity_pie_graph.addWidget(my_page_data_analyse_intensity_pie_graph_FC)

    # 将进度条重置为0
    set_ana_process_bar(0)
    init_draw_Objects()


def set_ana_process_bar(value: int):
    my_ui.my_page_data_analyse_progressBar.setValue(value)


# 态度图
def draw_analyse_attitude_tend(
        p_x: list,
        p_y: list,
        n_x: list,
        n_y: list
):
    """
    态度图\n
    将数据绘制到板子上

    :param p_x: 正向态度的x(日期)
    :param p_y: 正向态度的y(数据)
    :param n_x: 负向态度的x(日期)
    :param n_y: 负向态度的y(数据)
    :return: None
    """
    p_x_num = list(range(len(p_x)))
    my_page_data_analyse_attitude_tend_graph_ax.cla()
    my_page_data_analyse_attitude_tend_graph_ax.set_title("The Tend Graph of Attitude")
    for tick in my_page_data_analyse_attitude_tend_graph_ax.get_xticklabels():
        tick.set_rotation(300)
    my_page_data_analyse_attitude_tend_graph_ax.plot(p_x_num, p_y, label='Positive Value')
    my_page_data_analyse_attitude_tend_graph_ax.plot(n_x, n_y, label='Negative Value')
    my_page_data_analyse_attitude_tend_graph_ax.legend()
    my_page_data_analyse_attitude_tend_graph_FC.draw()


def draw_analyse_attitude_pie(
        p_x: int,
        n_x: int,
        p_x_str="Positive",
        n_x_str="Negative",
):
    """
    绘制饼图

    :param p_x:
    :param n_x:
    :param p_x_str:
    :param n_x_str:
    :return:
    """
    if p_x_str == "Positive":
        p_x_str += "(%d%%)" % (p_x * 100)
    if n_x_str == "Negative":
        n_x_str += "(%d%%)" % (n_x * 100)

    my_page_data_analyse_attitude_pie_graph_ax.cla()
    my_page_data_analyse_attitude_pie_graph_ax.set_title("The Pie of PN Attitude Value")
    print("正在画态度饼图")
    my_page_data_analyse_attitude_pie_graph_ax.pie(
        [
            p_x,
            n_x
        ], labels=[
            p_x_str,
            n_x_str
        ]
    )
    my_page_data_analyse_attitude_pie_graph_FC.draw()


# ###################激烈程度部分############################# #
# 激烈程度图
def draw_analyse_intensity_tend(
        i_x: list,
        i_y: list,
        none_x: list,
        none_y: list
):
    """
    激烈程度图\n
    将数据绘制到板子上

    :param i_x: 言辞激烈的x(日期)
    :param i_y: 言辞激烈的y(数据)
    :param none_x: 态度平平的x(日期)
    :param none_y: 态度平平的y(数据)
    :return: None
    """
    i_x_num = list(range(len(i_x)))
    my_page_data_analyse_intensity_tend_graph_ax.cla()
    my_page_data_analyse_intensity_tend_graph_ax.set_title("Tend of Intensity")
    my_page_data_analyse_intensity_tend_graph_ax.set_ylim((0, max(max(i_y), max(none_y))))
    for tick in my_page_data_analyse_intensity_tend_graph_ax.get_xticklabels():
        tick.set_rotation(300)
    my_page_data_analyse_intensity_tend_graph_ax.plot(i_x_num, i_y, label='Intensity Value')  # 这里注意，第一个是数字列表，第二个是字符列表
    my_page_data_analyse_intensity_tend_graph_ax.plot(none_x, none_y, label='Tiny Attitude Value')
    my_page_data_analyse_intensity_tend_graph_ax.legend()

    # my_page_data_analyse_intensity_tend_graph_ax.set_ylim((0, max(max(i_y), max(none_y))))
    # print("MAX: %d" % max(max(i_y), max(none_y)))
    # print(i_y)
    # print(i_x)
    # print(none_y)
    # print(none_x)
    my_page_data_analyse_intensity_tend_graph_FC.draw()


def draw_analyse_intensity_pie(
        i_x: int,
        none_x: int,
        i_x_str="Intense",
        none_x_str="Tiny Attitude",
):
    """
    绘制【激烈程度】饼图

    :param i_x:
    :param none_x:
    :param i_x_str:
    :param none_x_str:
    :return:
    """
    if i_x_str == "Intense":
        i_x_str += "(%d%%)" % (i_x * 100)
    if none_x_str == "Tiny Attitude":
        none_x_str += "(%d%%)" % (none_x * 100)

    my_page_data_analyse_intensity_pie_graph_ax.cla()
    my_page_data_analyse_intensity_pie_graph_ax.set_title("The Pie of Intensity")
    print("正在画激烈程度饼图")
    my_page_data_analyse_intensity_pie_graph_ax.pie(
        [
            i_x,
            none_x
        ], labels=[
            i_x_str,
            none_x_str
        ]
    )
    my_page_data_analyse_intensity_pie_graph_FC.draw()


def init_draw_Objects():
    print("初始化画图")
    draw_analyse_attitude_tend(
        p_x=[0],
        p_y=[0],
        n_x=[0],
        n_y=[0]
    )
    draw_analyse_intensity_tend(
        [0], [0], [0], [0]
    )
    draw_analyse_attitude_pie(
        p_x=100,
        p_x_str="waiting",
        n_x=0,
        n_x_str=""
    )
    draw_analyse_intensity_pie(
        i_x=0,
        i_x_str="",
        none_x=100,
        none_x_str="waiting"
    )


def obj_sort(my_dict: dict):
    cp = []
    for i in range(len(my_dict['date'])):
        cp.append([my_dict['date'][i], my_dict['data'][i]])

    cp.sort(key=lambda x: x[0])

    r = {
        'date': [],
        'data': []
    }
    for i in range(len(cp)):
        r['date'].append(cp[i][0])
        r['data'].append(cp[i][1])

    return r


def ana_start_draw():
    print("开始画图！")

    # 获取数据！
    P_json = obj_sort(analysis_processer.get_P())
    N_json = obj_sort(analysis_processer.get_N())
    I_json = obj_sort(analysis_processer.get_I())
    none_json = obj_sort(analysis_processer.get_none())

    # 画折线图！
    draw_analyse_attitude_tend(
        p_y=P_json['data'],
        p_x=P_json['date'],
        n_y=N_json['data'],
        n_x=N_json['date']
    )

    draw_analyse_intensity_tend(
        i_y=I_json['data'],
        i_x=I_json['date'],
        none_y=none_json['data'],
        none_x=none_json['date']
    )

    # 计算饼图数据
    p_sum = sum(list(P_json['data']))
    n_sum = sum(list(N_json['data']))

    i_sum = sum(list(I_json['data']))
    none_sum = sum(list(none_json['data']))

    if p_sum + n_sum > 0:
        p_per = p_sum / (p_sum + n_sum)
        n_per = n_sum / (p_sum + n_sum)
    else:
        p_per = 0.5
        n_per = 0.5

    if i_sum + none_sum > 0:
        i_per = i_sum / (i_sum + none_sum)
        none_per = none_sum / (i_sum + none_sum)
    else:
        i_per = 0.5
        none_per = 0.5

    # 画饼图
    draw_analyse_attitude_pie(p_x=p_per, n_x=n_per)
    draw_analyse_intensity_pie(i_x=i_per, none_x=none_per)

    # 画图完毕，重新启用按钮
    my_ui.my_page_data_analyse_commandLinkButton_start.setDisabled(False)
    my_ui.my_page_data_analyse_load_commandLinkButton.setDisabled(False)
    my_save()
    set_ana_process_bar(100)
    return


def set_process_text(my_str: str):
    my_ui.my_page_data_analyse_textEdit.setText(my_str)


def start_analyse():
    print("即将进行数据分析")

    if set_page_corpus_connect.is_run_available is False:
        print("你貌似没有通过校验！")
        QMessageBox.critical(my_ui.my_page_data_analyse, '错误', '你貌似还没有检验数据集的有效性', QMessageBox.Close)
        return

    base_path = set_page_corpus_connect.available_path
    if (
            os.path.isfile(os.path.join(base_path, "P.json")) and
            os.path.isfile(os.path.join(base_path, "N.json")) and
            os.path.isfile(os.path.join(base_path, "I.json")) and
            os.path.isfile(os.path.join(base_path, "none.json"))
    ) is True:
        user_l = QMessageBox.question(
            my_ui.my_page_data_analyse,
            "检测到现有的缓存...",
            "检测到了一个现有的缓存，是否从缓存中加载？\n选择 \"是\" 确认加载，选择 \"否\" 重新进行计算分析。\n如果选择\"取消\", 则不会做任何更改。",
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
            QMessageBox.Cancel
        )
        if user_l == QMessageBox.Yes:
            print("跳过计算，直接分析")
            ana_start_draw()
            return
        elif user_l == QMessageBox.Cancel:
            print("取消")
            return
    analysis_processer.analise_message.set_path(base_path)
    # 启动
    my_ui.my_page_data_analyse_commandLinkButton_start.setDisabled(True)
    my_ui.my_page_data_analyse_load_commandLinkButton.setDisabled(True)
    analysis_processer.analise_message.start()


def load():
    base_path = set_page_corpus_connect.available_path
    if (
            os.path.isfile(os.path.join(base_path, "P.json")) and
            os.path.isfile(os.path.join(base_path, "N.json")) and
            os.path.isfile(os.path.join(base_path, "I.json")) and
            os.path.isfile(os.path.join(base_path, "none.json"))
    ) is True:
        ana_start_draw()
        print("通过, 跳过计算")
    else:
        QMessageBox.warning(my_ui.my_page_data_analyse, "无缓存...", "注意，你没有一个可用的缓存可供加载！", QMessageBox.Close)
        return


def write_threshold():
    base_path = my_app_img_dir
    d = my_ui.my_page_data_analyse_doubleSpinBox.value()
    with open(os.path.join(base_path, "threshold.ini"), "w+") as f:
        f.write("%.2f" % d)
    print("已写入 %.2f" % d)


def set_default():
    my_ui.my_page_data_analyse_doubleSpinBox.setValue(1.5)


def my_save():
    base_path = my_app_img_dir
    my_page_data_analyse_attitude_tend_graph_fig.savefig(os.path.join(base_path, "ana_A.png"))
    my_page_data_analyse_attitude_pie_graph_fig.savefig(os.path.join(base_path, "ana_B.png"))
    my_page_data_analyse_intensity_tend_graph_fig.savefig(os.path.join(base_path, "ana_C.png"))
    my_page_data_analyse_intensity_pie_graph_fig.savefig(os.path.join(base_path, "ana_D.png"))
    print("ana ABCD img saved")
