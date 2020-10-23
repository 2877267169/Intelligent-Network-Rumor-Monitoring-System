"""
这个文件是连接QT界面的文件
放置信号与槽的设置代码
"""

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMessageBox

import set_page_corpus_connect
from analysis import analysis_start
import os, sys, json

test_obj = {
    "date": [
        "06-01",
        "06-02",
        "06-03",
        "06-04",
        "06-05"
    ],
    "data": [
        10,
        2,
        20,
        10,
        15
    ]
}
test_obj2 = {
    "date": [
        "06-01",
        "06-02",
        "06-03",
        "06-04",
        "06-05"
    ],
    "data": [
        15,
        10,
        20,
        2,
        10
    ]
}


def get_formatted_json_file(json_file_name: str):
    """
    获取经过格式化的json


    :param json_file_name:要获得的json文件，是 P.json, N.json, I.json, none.json中的一个。
    :return:
    """
    if os.path.isfile(
            os.path.join(set_page_corpus_connect.available_path, json_file_name)
    ) is True:
        with open(os.path.join(set_page_corpus_connect.available_path, json_file_name), 'r', encoding='utf-8') as f:
            my_obj: dict = json.load(f)
            for i in range(len(my_obj['date'])):
                my_obj['date'][i] = str(my_obj['date'][i])[5:] # 此处去掉了年份信息，然而不能现在去掉
                pass
        return my_obj
    else:
        return {"date": ["error"], "data": [0]}


def get_P():
    return get_formatted_json_file("P.json")


def get_N():
    return get_formatted_json_file("N.json")


def get_I():
    return get_formatted_json_file("I.json")


def get_none():
    return get_formatted_json_file("none.json")


my_ana_path = ""


class AnaliseMessage(QThread):
    s_send_analyse_process_bar = pyqtSignal(int)
    s_send_analyse_process_text = pyqtSignal(str)
    s_send_analyse_start_draw = pyqtSignal()

    def f_send_my_analyse_process_bar(self, value: int):
        self.s_send_analyse_process_bar.emit(value)

    def f_send_text_message(self, my_text: str):
        self.s_send_analyse_process_text.emit(my_text)

    def set_path(self, path: str):
        global my_ana_path
        my_ana_path = path

    def run(self):
        global my_ana_path
        if my_ana_path == "":
            print("错误：未传入路径")
            return
        ana_start(my_ana_path)


analise_message = AnaliseMessage()


def ana_start(path=""):
    if path == "":
        print("error, 未传入路径")
        return
    print("分析进程已经开始")
    """
    if os.path.isfile(
        os.path.join(
            path,
            "P.json"
        )
    ) is True:
        r = QMessageBox.question(my_ui.my_page_train_tp_pushButtton_clear_and_set_to_default, "警告", '你确定要重置参数为默认参数吗？',
                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)"""
    analise_message.f_send_text_message("正在准备开始")
    # #########开始了！####### #
    analysis_start.start(path)

    print("分析结束！")
    analise_message.s_send_analyse_start_draw.emit()
    analise_message.f_send_my_analyse_process_bar(100)
