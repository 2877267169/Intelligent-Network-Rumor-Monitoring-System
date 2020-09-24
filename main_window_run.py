import os, sys
import MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow
import ui_change
import set_page_corpus_connect
import set_page_train_connect
import set_page_hot_connect
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

def set_all_connect(ui: MainWindow):
    print('set_page_corpus_connect')
    set_page_corpus_connect.set_page_corpus_connect(ui=ui)
    print("set_page_train_connect")
    set_page_train_connect.set_page_train_connect(ui=ui)
    print("set_page_train_connect")
    set_page_hot_connect.set_page_connect(ui=ui)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    ui = MainWindow.Ui_MainWindow()
    ui.setupUi(main_window)
    ui_change.set_connect(ui=ui)
    ui.stackedWidget.setCurrentIndex(0)

    set_all_connect(ui) # 设置全部的信号与槽的链接

    main_window.show()
    sys.exit(app.exec_())
