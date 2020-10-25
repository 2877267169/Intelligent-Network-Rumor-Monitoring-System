"""
开通测试分支1
2020-10-13 22:53:53 李建广 加入了测试
改名测试，克隆分支测试
"""
import os, sys
my_app_data = os.path.join(os.getenv("appdata"), "INRMS")
if os.path.isdir(my_app_data) is False:
    os.makedirs(my_app_data)

import MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow
import ui_change
import set_page_corpus_connect
import set_page_train_connect
import set_page_hot_connect
import set_page_data_analyse_connect
import matplotlib

matplotlib.use("Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"



def f_debug():
    """
    会在调试变量为True时候执行本函数
    """
    my_debug = "False"

    if os.path.isfile(os.path.join(my_app_data, "DEBUG")) is False:
        with open(os.path.join(my_app_data, "DEBUG"), 'w+', encoding='utf-8') as f:
            f.write("False")
        my_debug = "False"
    else:
        with open(os.path.join(my_app_data, "DEBUG"), 'r', encoding='utf-8') as f:
            a = f.readline().replace('\n', '')
        my_debug = a

    if my_debug != "True":
        # 有且仅有my_debug==True的时候，下面的代码才会执行！
        ui.frame_8.setVisible(False)  # 检测报告
        ui.frame_2.setVisible(False)  # 谣言预警


def set_all_connect(ui: MainWindow):
    print('set_page_corpus_connect')
    set_page_corpus_connect.set_page_corpus_connect(ui=ui)
    print("set_page_train_connect")
    set_page_train_connect.set_page_train_connect(ui=ui)
    print("set_page_train_connect")
    set_page_hot_connect.set_page_connect(ui=ui)
    print("set_page_data_analise_connect")
    set_page_data_analyse_connect.set_page_data_analyse_connect(ui=ui)

    f_debug()


if __name__ == '__main__':
    ui = MainWindow.Ui_MainWindow()
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    # ui = MainWindow.Ui_MainWindow() # 【注意】，这句话提到了前面成为全局变量
    ui.setupUi(main_window)
    ui_change.set_connect(ui=ui)
    ui.stackedWidget.setCurrentIndex(0)

    set_all_connect(ui)  # 设置全部的信号与槽的链接

    main_window.show()
    sys.exit(app.exec_())
