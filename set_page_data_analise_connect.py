from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
import os, sys

import MainWindow
from data import transform_json_to_txt
from data import bert_train_complex
import running_state
import json

# matplotlib 和qt链接的包
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

# 画图对象
my_page_data_analise_attitude_tend_graph_fig = plt.figure()
# 利用对象构建组件
my_page_data_analise_attitude_tend_graph_FC = FigureCanvas(my_page_data_analise_attitude_tend_graph_fig)
# 真正画图的东西
my_page_data_analise_attitude_tend_graph_ax = my_page_data_analise_attitude_tend_graph_fig.add_subplot(1, 1, 1)


def set_page_data_analise_connect(ui: MainWindow.Ui_MainWindow):
    init_graph()


def init_graph():
    pass
