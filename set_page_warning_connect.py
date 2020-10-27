from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import os, sys

import MainWindow
from analysis.analysis_processer import get_4_percentage
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
my_page_warning_fig = plt.figure()

# 利用对象构建组件
my_page_warning_FC = FigureCanvas(my_page_warning_fig)

# 真正画图的东西
my_page_warning_ax = my_page_warning_fig.add_subplot(1, 1, 1)


def set_warning_connect(ui: MainWindow.Ui_MainWindow):
    global my_ui
    my_ui = ui
    # 设置信号与槽的链接
    ui.my_page_warning_start_commandLinkButton.clicked.connect(start_to_warning)

    # 将画板加入组件
    ui.my_page_warning_graph.layout().addWidget(my_page_warning_FC)

    init_graph()


def init_graph():
    zero_obj = {"date": [0], "data": [0]}
    draw_graph(zero_obj, zero_obj, zero_obj, zero_obj)


def draw_graph(P: dict, N: dict, I: dict, none: dict):
    base_dir = my_app_img_dir
    my_page_warning_ax.cla()
    my_page_warning_ax.set_title("Normalized data analysis")
    p_x = list(range(len(P["date"])))
    my_page_warning_ax.plot(p_x, P["data"], linestyle='none', marker='P', color="orange", label="Positive Value")
    my_page_warning_ax.plot(p_x, N["data"], linestyle='none', marker='P', color="blue", label="Negative Value")
    my_page_warning_ax.plot(p_x, I["data"], linestyle='none', marker='x', color="red", label="Intensity Value")
    my_page_warning_ax.plot(p_x, none["data"], linestyle='none', marker='x', color="green", label="Tiny Attitude Value")
    for tick in my_page_warning_ax.get_xticklabels():
        tick.set_rotation(300)
    my_page_warning_ax.legend()
    my_page_warning_FC.draw()
    my_page_warning_fig.savefig(os.path.join(base_dir, "warning.png"))
    print("warning saved")


def loud_from_file_to_graph():
    return get_4_percentage()


def start_to_warning():
    print("分析命令开始")
    # 进行百分比趋势分析

    # 画图
    l: list = loud_from_file_to_graph()
    draw_graph(l[0], l[1], l[2], l[3])
