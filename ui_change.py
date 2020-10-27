from PyQt5 import QtCore, QtGui, QtWidgets
import MainWindow
import set_page_train_connect
import set_page_corpus_connect



def set_connect(ui: MainWindow.Ui_MainWindow):
    global my_ui
    print('正在设置')
    my_ui = ui
    print(ui)
    ui.my_train_button.clicked.connect(change_to_train)
    ui.my_corpus_button.clicked.connect(change_to_corpus)
    ui.my_data_analize_button.clicked.connect(change_to_data)
    ui.my_warning_button.clicked.connect(change_to_warning)
    ui.my_hot_word_button.clicked.connect(change_to_hot)
    # ui.my_paper_button.clicked.connect(change_to_paper)


def change_to_corpus():
    global my_ui
    print(0)

    my_ui.stackedWidget.setCurrentIndex(0)
    set_page_corpus_connect.re_draw()


def change_to_train():
    print(1)
    my_ui.stackedWidget.setCurrentIndex(1)
    set_page_train_connect.re_draw()


def change_to_data():
    print(2)
    my_ui.stackedWidget.setCurrentIndex(2)


def change_to_warning():
    print(3)
    my_ui.stackedWidget.setCurrentIndex(3)


def change_to_hot():
    print(4)
    my_ui.stackedWidget.setCurrentIndex(4)



