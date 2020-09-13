import os, sys
import MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow
import ui_change

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    ui = MainWindow.Ui_MainWindow()
    ui.setupUi(main_window)
    ui_change.set_connect(ui=ui)
    ui.stackedWidget.setCurrentIndex(0)

    main_window.show()
    exit(app.exec_())
