"""
针对ui界面进行了修改以连接界面

"""

import os

from PyQt5.QtCore import QThread, pyqtSignal

from data.data_ops import Data_ops as Data


def get_file_context(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as f:
        l = f.readlines()
    res = ""
    for s in l:
        res += s
    res.replace('\n', '')
    line = res.split('\t')
    res = (line[0] + '\t' + line[-1])
    return res


def main_run(base_dir: str):
    # base_dir = r"C:\Users\john\Desktop\repos\标注综合\顶替_大学"

    data = Data(base_dir)
    all_file_name = data.get_all_path()
    cnt = 0
    with open(os.path.join(base_dir, "bert_train.tsv"), 'w+', encoding='utf-8') as f:
        f_dev = open(os.path.join(base_dir, "bert_dev.tsv"), 'w+', encoding='utf-8')
        f_test = open(os.path.join(base_dir, "bert_test.tsv"), 'w+', encoding='utf-8')

        p_list = []
        n_list = []
        res_list = []
        for file_path in all_file_name:
            words = get_file_context(file_path=file_path).replace('\n', '')
            label = data.get_file_text(
                data.transforme_to_mark_file_path(base_dir=base_dir, file_path_list=[file_path])[0])
            l = map(int, label.split('-'))
            for i in l:
                if i != 0:
                    label = '1'
                else:
                    label = '0'

            if label == '1':
                p_list.append("%s\t%s\n" % (label, words))
            else:
                n_list.append("%s\t%s\n" % (label, words))

        p_len = len(p_list)
        res_list += p_list
        res_list += n_list[:int((p_len) * 2)]
        res_list.sort(key=lambda x: x.split('\t')[2])
        for line in res_list:
            f.write(line)
            if cnt % 2 == 0:
                f_test.write(line)
            if cnt % 3 == 0:
                f_dev.write(line)
            cnt += 1
            if cnt % 100 == 0:
                thread_train_comp.send_message(str(cnt))
                print(cnt)
        thread_train_comp.send_message("已完成，共处理 %d 条记录" % cnt)
        print("已完成，共处理 %d 条记录" % cnt)
        f_test.close()
        f_dev.close()


class Thread_train_comp(QThread):
    my_send_message = pyqtSignal(str, str)

    def set_args(self, base_dir: str):
        self.base_dir = base_dir

    def send_message(self, message_str, end='\n'):
        self.my_send_message.emit(message_str, end)

    def run(self):
        main_run(self.base_dir)


thread_train_comp = Thread_train_comp()
