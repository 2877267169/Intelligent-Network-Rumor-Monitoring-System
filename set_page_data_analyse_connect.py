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
    analysis_processer.analise_message.send_analyse_process_bar.connect(set_ana_process_bar)

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
    my_page_data_analyse_attitude_tend_graph_ax.cla()
    my_page_data_analyse_attitude_tend_graph_ax.set_title("The Tend Graph of Attitude")
    for tick in my_page_data_analyse_attitude_tend_graph_ax.get_xticklabels():
        tick.set_rotation(300)
    my_page_data_analyse_attitude_tend_graph_ax.plot(p_x, p_y)
    my_page_data_analyse_attitude_tend_graph_ax.plot(n_x, n_y)
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
    my_page_data_analyse_attitude_pie_graph_ax.cla()
    my_page_data_analyse_attitude_pie_graph_ax.set_title("The Pie of PN Attitude")
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
    my_page_data_analyse_intensity_tend_graph_ax.cla()
    my_page_data_analyse_intensity_tend_graph_ax.set_title("Tend of Intensity")
    for tick in my_page_data_analyse_intensity_tend_graph_ax.get_xticklabels():
        tick.set_rotation(300)
    my_page_data_analyse_intensity_tend_graph_ax.plot(i_x, i_y)
    my_page_data_analyse_intensity_tend_graph_ax.plot(none_x, none_y)
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
    print("测试画图")
    draw_analyse_attitude_tend(
        p_y=analysis_processer.get_P()['data'],
        p_x=analysis_processer.get_P()['date'],
        n_y=analysis_processer.get_N()['data'],
        n_x=analysis_processer.get_N()['date']
    )
    draw_analyse_attitude_pie(
        60, 40
    )
    draw_analyse_intensity_tend(
        i_y=analysis_processer.get_P()['data'],
        i_x=analysis_processer.get_P()['date'],
        none_y=analysis_processer.get_N()['data'],
        none_x=analysis_processer.get_N()['date']
    )
    draw_analyse_intensity_pie(
        60, 40
    )

    print("我被执行了！")


def start_analyse():
    print("即将进行数据分析")
    if set_page_corpus_connect.is_run_available is False:
        print("你貌似没有通过校验！")
        QMessageBox.critical(my_ui.my_page_data_analyse, '错误', '你貌似还没有检验数据集的有效性', QMessageBox.Close)
        return
    analysis_processer.analise_message.set_path(set_page_corpus_connect.available_path)
    # 启动
    analysis_processer.analise_message.start()
