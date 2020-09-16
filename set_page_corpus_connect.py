import threading

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
import os, sys

import MainWindow
from data import transform_json_to_txt

is_run_available = False

my_ui = MainWindow.Ui_MainWindow()


def set_page_corpus_connect(ui: MainWindow.Ui_MainWindow):
    global my_ui
    my_ui = ui

    # 按钮
    ui.my_page_corpus_button_fromJson.clicked.connect(get_user_input_and_set_to_json_lineEdit)
    ui.my_page_corpus_button_workDir.clicked.connect(get_user_input_and_set_to_workDir)
    ui.my_page_corpus_button_directionary.clicked.connect(get_user_input_and_set_to_directionary_lineEdit)

    # 命令按钮
    ui.my_page_corpus_commandLinkButton_verify.clicked.connect(verify_files)
    ui.my_page_corpus_commandLinkButton_go_for_work_space.clicked.connect(create_work_space)

    # 文本框
    ui.my_page_corpus_lineEdit_from_json.textChanged.connect(set_run_unavailable)
    ui.my_page_corpus_lineEdit_directory.textChanged.connect(set_run_unavailable)
    ui.my_page_corpus_lineEdit_workPath.textChanged.connect(set_run_unavailable)

    # 消息传递
    transform_json_to_txt.thread_transform_json_to_txt.my_send_message.connect(ptr_message)
    transform_json_to_txt.thread_transform_json_to_txt.my_send_process_bar_message.connect(set_process_bar)

def get_user_input_and_set_to_json_lineEdit():
    global my_ui
    file_path, file_type = QFileDialog.getOpenFileName(my_ui.my_page_corpus_lineEdit_from_json, "Select json file", '.',
                                                       "json file(*.json)")
    my_ui.my_page_corpus_lineEdit_from_json.setText(file_path)


def get_user_input_and_set_to_workDir():
    global my_ui
    dir_path = QFileDialog.getExistingDirectory(my_ui.my_page_corpus_lineEdit_workPath, "Select work dir", '.')
    my_ui.my_page_corpus_lineEdit_workPath.setText(dir_path)


def get_user_input_and_set_to_directionary_lineEdit():
    global my_ui
    file_path, file_type = QFileDialog.getOpenFileName(my_ui.my_page_corpus_lineEdit_directory, "Select txt file", '.',
                                                       "txt file(*.txt)")
    my_ui.my_page_corpus_lineEdit_directory.setText(file_path)


def verify_files():
    global my_ui
    global is_run_available
    json_file_path = my_ui.my_page_corpus_lineEdit_from_json.text()
    work_path = my_ui.my_page_corpus_lineEdit_workPath.text()
    dictionary = my_ui.my_page_corpus_lineEdit_directory.text()

    if os.path.isfile(json_file_path) and os.path.isdir(work_path) and (dictionary == '' or os.path.isfile(dictionary)):
        # 校验成功
        ptr_message('校验成功')
        is_run_available = True
    else:
        ptr_message('校验失败！请检查路径')
        is_run_available = False


def set_run_unavailable():
    # 在手动更改了框内的路径时被调用
    global is_run_available
    is_run_available = False
    ptr_message('更改了路径后，应当重新校验。')


def ptr_message(mystr: str, end='\n'):
    global my_ui
    my_ui.my_page_corpus_textEdit.setText("%s%s%s" % (mystr, end, my_ui.my_page_corpus_textEdit.toPlainText()))


def set_process_bar(proc:int):
    my_ui.my_page_corpus_ProcessBar.setValue(proc)


def create_work_space():
    print('create_work_space')
    global is_run_available
    if is_run_available is False:
        ptr_message("你的更改的内容没有进行校验，请先进行校验！")
        return

    global my_ui
    work_path = my_ui.my_page_corpus_lineEdit_workPath.text()
    json_path = my_ui.my_page_corpus_lineEdit_from_json.text()

    transform_json_to_txt.thread_transform_json_to_txt.set_args(json_file_path=json_path, out_put_dir=work_path, moudle_name='')
    transform_json_to_txt.thread_transform_json_to_txt.start()


