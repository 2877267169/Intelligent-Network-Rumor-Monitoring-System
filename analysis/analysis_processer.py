from PyQt5.QtCore import QThread, pyqtSignal

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


def get_P():
    return test_obj


def get_N():
    return test_obj2


def get_I():
    return test_obj


def get_none():
    return test_obj


my_ana_path = ""


class AnaliseMessage(QThread):
    send_analyse_process_bar = pyqtSignal(int)

    def f_send_my_analyse_process_bar(self, value: int):
        self.send_analyse_process_bar.emit(value)

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
    analise_message.f_send_my_analyse_process_bar(66)
