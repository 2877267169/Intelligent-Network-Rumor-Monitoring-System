import os
import LAC
from PyQt5.QtCore import QThread, pyqtSignal

from data.data_ops import Data_ops as Data
import set_page_hot_connect
from data import data_ops

dic = {}  # 全局字典变量
lac = LAC.LAC()


def cnt_words(cnt_file_path: str):
    global dic

    with open(cnt_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    cnt_1 = 0
    all_1 = len(lines)

    for line in lines:
        line = line.replace('的', '').replace('啊', '').replace('吧', '').replace('，', '').replace('！', '').replace(
            '。', '').replace('；', '').replace('#', '').replace('?', '').replace('了', '').replace('吗', '').split('\t')[-1]
        lac_res = lac.run(line)
        wordL = lac_res[0]
        # if cnt_1%17 == 0:
            # word_cloude_create.send_process(int(30+(30*(cnt_1/all_1))))
        for word in wordL:
            if list(dic.keys()).count(word) == 0:
                dic[word] = 1
            else:
                dic[word] = dic[word] + 1
    return dic


class WordCloudeCreate(QThread):
    send_cloude_dict = pyqtSignal(dict, dict)
    send_graph_process_bar = pyqtSignal(int)

    def set_path(self, path: str):
        self.path = path

    def run(self):
        global dic
        dic = {}
        # word_cloude_create.send_process(20)
        if os.path.isfile(os.path.join(self.path, 'index.txt')) is False:
            print("Error, no index.txt")
            return
        data = data_ops.Data_ops(self.path)
        cnt_0 = 0
        all_0 = len(data.get_all_path())
        for file_path in data.get_all_path():
            word_cloude_create.send_process(int((50 * (cnt_0 / all_0))))
            cnt_words(cnt_file_path=file_path)
            cnt_0+=1

        dic_b = dic.copy()
        list_b = []
        for key in list(dic_b.keys()):
            list_b.append([key, dic_b[key]])
        list_b.sort(key=lambda x: x[1])
        list_b = list_b[:-20]
        dic_b.clear()
        cnt_2 = 0
        all_2 = len(list_b)
        for line in list_b:
            if cnt_2 %100 == 0:
                word_cloude_create.send_process(int(50+(50*(cnt_2/all_2))))
                print("working for %s..."%line[0])
            dic_b[line[0]] = line[1]
            cnt_2 += 1
        word_cloude_create.send_process(100)
        self.send_cloude_dict.emit(dic, dic_b)

    def send_process(self, step_process:int):
        self.send_graph_process_bar.emit(step_process)


word_cloude_create = WordCloudeCreate()
