from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import os, sys

import MainWindow
import set_page_corpus_connect
from analysis.analysis_processer import get_4_percentage
from analysis.read_from_bert import get_bert_res_to_json
from data import transform_json_to_txt
from data import bert_train_complex
import running_state
import json
from warning import wcalc
from analysis import analysis_processer
# matplotlib 和qt链接的包
# 修复打包的问题
import matplotlib

from main_window_run import my_app_img_dir
from set_page_data_analyse_connect import obj_sort
from set_page_train_connect import get_all_file_parameters, file_parameters

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
    draw_graph(zero_obj, zero_obj, zero_obj, zero_obj, zero_obj)


def draw_graph(P: dict, N: dict, I: dict, none: dict, bert_res=None):
    if bert_res is None:
        bert_res = {"date": [0], "data": [0]}
    base_dir = my_app_img_dir
    my_page_warning_ax.cla()
    my_page_warning_ax.set_title("Normalized data analysis")
    p_x = list(range(len(P["date"])))
    my_page_warning_ax.plot(p_x, P["data"], linestyle='none', marker='P', color="orange", label="Positive Value")
    my_page_warning_ax.plot(p_x, N["data"], linestyle='none', marker='P', color="blue", label="Negative Value")
    my_page_warning_ax.plot(p_x, I["data"], linestyle='none', marker='x', color="red", label="Intensity Value")
    my_page_warning_ax.plot(p_x, none["data"], linestyle='none', marker='x', color="lightseagreen",
                            label="Tiny Attitude Value")
    my_page_warning_ax.plot(bert_res["date"], bert_res["data"], linestyle='none', marker='.',
                            color="green", label="BERT Model res")
    for tick in my_page_warning_ax.get_xticklabels():
        tick.set_rotation(300)
    my_page_warning_ax.legend()
    my_page_warning_FC.draw()
    my_page_warning_fig.savefig(os.path.join(base_dir, "warning.png"))
    print("warning saved")


def loud_from_file_to_graph():
    return get_4_percentage()


def start_to_warning():
    global my_ui

    print("分析命令开始")
    paras = get_all_file_parameters()
    work_path = set_page_corpus_connect.available_path
    res_path = os.path.join(paras[file_parameters.output_dir], "test_results.tsv")
    # 画图
    my_ui.my_page_warning_progressBar.setValue(20)


    if os.path.isfile(res_path) is False:
        print("找不到训练结果文件！%s" % res_path)
        QMessageBox.critical(
            my_ui.stackedWidget,
            '错误',
            "\"%s\"\n找不到训练结果文件！" % res_path,
            QMessageBox.Close
        )
        my_ui.my_page_warning_progressBar.setValue(0)
        return
    if os.path.isdir(work_path) is False:
        print("工作路径有问题，请检查是否已完成语料设置%s" % work_path)
        QMessageBox.critical(
            my_ui.stackedWidget,
            '错误',
            "\"%s\"\n工作路径有问题，请检查是否已完成语料设置" % work_path,
            QMessageBox.Close
        )
        my_ui.my_page_warning_progressBar.setValue(0)
        return
    l: list = loud_from_file_to_graph()
    get_bert_res_to_json(work_path=set_page_corpus_connect.available_path,
                         bert_train_res_file_path=os.path.join(paras[file_parameters.output_dir], "test_results.tsv"))
    if os.path.isfile(os.path.join(work_path, "toal.json")) is True:
        print("成功检测到结果文件 %s ,现在画图" % os.path.join(work_path, "toal.json"))
        with open(os.path.join(work_path, "toal.json"), 'r', encoding='utf-8') as f:
            my_obj = json.load(f)
        my_out_obj = obj_sort({"date": my_obj[0], "data": my_obj[1]})
        tmp = ""
        count = 0
        for i in range(len(my_out_obj["date"])):
            if my_out_obj["date"][i] != tmp:
                tmp = my_out_obj["date"][i]
                my_out_obj["date"][i] = count
                count += 1
            else:
                my_out_obj["date"][i] = count
        a = list(set(my_out_obj["date"]))
        draw_graph(l[0], l[1], l[2], l[3], my_out_obj)
        # return 此处不返回
    else:
        QMessageBox.critical(
            my_ui.stackedWidget,
            '错误',
            "执行完毕，但%s生成存在问题。" % os.path.join(work_path, "toal.json"),
            QMessageBox.Close
        )
        print("执行完毕，但%s生成存在问题。" % os.path.join(work_path, "toal.json"))
        my_ui.my_page_warning_progressBar.setValue(0)
        return
    # 进行百分比趋势分析
    my_ui.my_page_warning_progressBar.setValue(50)
    wcalc.warning_start(n=l[1]["data"], i=l[2]["data"], work_path=work_path)
    if os.path.isfile(os.path.join(work_path, "warning.json")) is False:
        QMessageBox.critical(
            my_ui.stackedWidget,
            '错误',
            "执行完毕，但%s的生成存在问题。" % os.path.join(work_path, "warning.json"),
            QMessageBox.Close
        )
        my_ui.my_page_warning_progressBar.setValue(0)
        return
    my_w_out = wcalc.get_obj(work_path=work_path)
    my_ui.my_page_warning_see_textEdit.setText(str(my_w_out))
    my_ui.my_page_warninig_message_text_edit.setText(str("危"))
    my_ui.my_page_warning_progressBar.setValue(100)
    return
