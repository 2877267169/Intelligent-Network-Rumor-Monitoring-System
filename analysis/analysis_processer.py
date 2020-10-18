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


def ana_start(path:str):
    pass


class AnaliseMessage(QThread):
    send_analise_process_bar = pyqtSignal(int)


analise_message = AnaliseMessage()
