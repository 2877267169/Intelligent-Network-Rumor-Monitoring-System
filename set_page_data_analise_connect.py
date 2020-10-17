from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
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
my_page_data_analise_attitude_tend_graph_fig = plt.figure()
my_page_data_analise_attitude_pie_graph_fig = plt.figure()
my_page_data_analise_intensity_tend_graph_fig = plt.figure()
my_page_data_analise_intensity_pie_graph_fig = plt.figure()
# 利用对象构建组件
my_page_data_analyse_attitude_tend_graph_FC = FigureCanvas(my_page_data_analise_attitude_tend_graph_fig)
my_page_data_analyse_attitude_pie_graph_FC = FigureCanvas(my_page_data_analise_attitude_pie_graph_fig)
my_page_data_analyse_intensity_tend_graph_FC = FigureCanvas(my_page_data_analise_intensity_tend_graph_fig)
my_page_data_analyse_intensity_pie_graph_FC = FigureCanvas(my_page_data_analise_intensity_pie_graph_fig)
# 真正画图的东西
my_page_data_analise_attitude_tend_graph_ax = my_page_data_analise_attitude_tend_graph_fig.add_subplot(1, 1, 1)
my_page_data_analise_attitude_pie_graph_ax = my_page_data_analise_attitude_pie_graph_fig.add_subplot(1, 1, 1)
my_page_data_analise_intensity_tend_graph_ax = my_page_data_analise_intensity_tend_graph_fig.add_subplot(1, 1, 1)
my_page_data_analise_intensity_pie_graph_ax = my_page_data_analise_intensity_pie_graph_fig.add_subplot(1, 1, 1)

my_ui = MainWindow.Ui_MainWindow()


def set_page_data_analise_connect(ui: MainWindow.Ui_MainWindow):
    global my_ui
    my_ui = ui
    ui.my_page_data_analize_commandLinkButton_start.clicked.connect(start_analise)

    # 加入组件的操作
    ui.my_page_data_analyse_attitude_tend_graph.layout().addWidget(my_page_data_analyse_attitude_tend_graph_FC)
    ui.my_page_data_analyse_attitude_pie_graph.addWidget(my_page_data_analyse_attitude_pie_graph_FC)
    ui.my_page_data_analyse_intensity_tend_graph.addWidget(my_page_data_analyse_intensity_tend_graph_FC)
    ui.my_page_data_analyse_intensity_pie_graph.addWidget(my_page_data_analyse_intensity_pie_graph_FC)

    init_draw_Objects()


# 态度图
def draw_analise_attitude_tend(
        p_x: list,
        p_y: list,
        n_x: list,
        n_y: list
):
    """
    将数据绘制到板子上

    :param p_x: 正向态度的x(日期)
    :param p_y: 正向态度的y(数据)
    :param n_x: 负向态度的x(日期)
    :param n_y: 负向态度的y(数据)
    :return: None
    """
    my_page_data_analise_attitude_tend_graph_ax.cla()
    my_page_data_analise_attitude_tend_graph_ax.set_title("The Tend Graph of Attitude")
    for tick in my_page_data_analise_attitude_tend_graph_ax.get_xticklabels():
        tick.set_rotation(300)
    my_page_data_analise_attitude_tend_graph_ax.plot(p_x, p_y)
    my_page_data_analise_attitude_tend_graph_ax.plot(n_x, n_y)
    my_page_data_analyse_attitude_tend_graph_FC.draw()


def init_draw_Objects():
    print("测试画图")
    draw_analise_attitude_tend(
        p_y=analysis_processer.get_P()['data'],
        p_x=analysis_processer.get_P()['date'],
        n_y=analysis_processer.get_N()['data'],
        n_x=analysis_processer.get_N()['date']
    )

    print("我被执行了！")


def start_analise():
    print("正在进行数据分析")
