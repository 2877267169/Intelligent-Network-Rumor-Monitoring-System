"""

数据集格式转化工具 版本1.0
将json文件转化成可读的txt文件

"""
from PyQt5.QtCore import QThread, pyqtSignal
import running_state

"""
针对GUI界面进行了优化
"""
import threading
import json
import os
import time
import MainWindow
import set_page_corpus_connect


## 注意，必须运行此函数，不然无法连接界面！
def setUI(ui: MainWindow.Ui_MainWindow):
    global my_ui
    my_ui = ui


# 全局统计用字典
# 他应该再开始时候被重置。
g_sum_dict = {}

show_times = 17 # 进度条展示频率

def make_statistics(my_date: str):
    global g_sum_dict
    if (my_date in g_sum_dict) is False:
        g_sum_dict[my_date] = 1
    else:
        g_sum_dict[my_date] += 1


def submit_dict():
    global g_sum_dict
    # submit
    thread_transform_json_to_txt.send_dict_for_graph(g_sum_dict)


#
def sim_forment_time_str(time_str: str):
    l = time_str.split('-')
    return "%04d-%02d-%02d" % (int(l[0]), int(l[1]), int(l[2]))


def chick_dictionary(a_weibo: dict):
    min_time_str = sim_forment_time_str(a_weibo['date'])
    min_time = int(min_time_str.replace('-', ''))
    for reply in a_weibo['reply']:
        reply_time_str = sim_forment_time_str(reply['date'])
        reply_time = int(reply_time_str.replace('-', ''))
        if reply_time < min_time:
            min_time = reply_time
            min_time_str = reply_time_str
    a_weibo['date'] = min_time_str
    return a_weibo


def show_time(start_t, p):
    now_t = time.time()
    t = now_t - start_t
    ana = (t / p) * (1 - p)
    thread_transform_json_to_txt.my_sender("已用时 %.2f 秒(%.1f 分钟)" % (t, t / 60), end='')
    thread_transform_json_to_txt.my_sender(
        "预计剩余 %.2f 秒(%.1f 分钟)，\n预计完成时间 %s." % (ana, ana / 60, time.asctime(time.localtime(now_t + ana))))


def form_time(time_str: str):
    l = time_str.split('-')
    my_formatted_str = "%04d-%02d-%02d" % (int(l[0]), int(l[1]), int(l[2]))
    make_statistics(my_formatted_str[-5:])
    return my_formatted_str


def main_run(json_file_path: str, out_put_dir: str, moudle_name: str):
    global show_times
    global g_sum_dict
    # start 注意：这是修改后的内容#在此注释中间的内容谨慎修改！2020年7月27日16:37:55##################################################
    # out_put_dir = ""
    thread_transform_json_to_txt.my_sender(json_file_path)
    """if is_auto_path_name is False:
        print(out_put_dir)#" = input("请输入输出文件夹").replace('"', '')"
    else:
        out_put_dir = "json_to_txt_out_put/json_to_txt_%d" % time.time()"""
    """if os.path.exists(out_put_dir):
        print("已经存在了，取消")
        return"""
    """else:
        print(out_put_dir + " 是合法的路径.")"""
    out_put_dir = os.path.join(out_put_dir, moudle_name)  # 注意！在这里面加了模块名！
    thread_transform_json_to_txt.my_sender("将在\n    %s\n 目录内进行操作" % out_put_dir)
    """c = input()
    if (c != 'y') and (c != 'Y'):
        return"""
    #####注意， 由于不再新建文件夹，此处将其注释掉
    # os.makedirs(out_put_dir)

    if os.path.isdir(os.path.join(out_put_dir, "reply")) is False:
        os.makedirs(os.path.join(out_put_dir, "reply"))
    else:
        thread_transform_json_to_txt.my_sender('***警告*** 将会覆盖工作空间')
        print("***警告*** 将会覆盖工作空间")
    thread_transform_json_to_txt.my_sender("已建立文件夹")
    reply_out_put_dir = os.path.join(out_put_dir, "reply")
    # End注意：这是修改后的内容#在此注释中间的内容谨慎修改！2020年7月27日16:37:55#################################################

    myobj = json.load(open(json_file_path, 'r', encoding='utf-8'))
    myobj.remove(myobj[-1])
    start_t = time.time()  # 开始
    all_num = len(myobj)  # 总长度
    index = 1
    reply_index = 1

    f_index_txt = open(os.path.join(out_put_dir, "index.txt"), 'w+', encoding='utf-8')
    for weiboDirectory in myobj:
        weiboDirectory = chick_dictionary(weiboDirectory)
        mytime = form_time(weiboDirectory["date"])
        weiboDirectory_name = "%s_%03d_%04d" % (mytime, index, weiboDirectory['reply_num'])

        f_index_txt.write("%s.txt\n" % weiboDirectory_name)  # 向索引写入一条记录！
        with open(os.path.join(out_put_dir, "%s.txt" % weiboDirectory_name), "w+", encoding="utf-8") as f:
            f.write("%s\t%s\t%d\t%s" % (
                mytime,
                weiboDirectory["username"],
                weiboDirectory["reply_num"],
                weiboDirectory["text"]
            ))
        if os.path.isdir(os.path.join(reply_out_put_dir, weiboDirectory_name)) is False:
            os.makedirs(
                os.path.join(reply_out_put_dir, weiboDirectory_name)
            )
        reply_index = 1
        # 遍历回复！
        reply_index_txt = open(
            os.path.join(
                reply_out_put_dir,
                weiboDirectory_name,
                "reply_index.txt"
            ),
            'w+',
            encoding='utf-8'
        )
        for reply_obj in weiboDirectory["reply"]:
            reply_time = form_time(reply_obj["date"])
            reply_index_txt.write("%s_%03d.txt\n" % (reply_time, reply_index))
            with open(
                    os.path.join(
                        reply_out_put_dir,
                        weiboDirectory_name,
                        "%s_%03d.txt" % (reply_time, reply_index)
                    ).replace('/', '\\'), "w+", encoding="utf-8"
            ) as f:
                f.write("%s\t%s\t%d\t%s" % (
                    reply_time,
                    reply_obj["username"],
                    reply_obj["reply_num"],
                    reply_obj["text"]
                ))
                reply_index += 1
        reply_index_txt.close()
        show_times = all_num//17
        if index % show_times == 0:
            submit_dict()
            thread_transform_json_to_txt.my_sender("\n已完成%.2f%%" % ((index / all_num) * 100))
            print("已完成%.2f%%" % ((index / all_num) * 100))
            thread_transform_json_to_txt.send_process(int((index / all_num) * 100))
            show_time(start_t=start_t, p=(index / all_num))
        index += 1
    f_index_txt.close()
    thread_transform_json_to_txt.my_sender("Done.")
    thread_transform_json_to_txt.send_process(100)


# main_run(json_file_path=json_file_path, out_put_dir=out_put_dir_path, moudle_name=moudle_name)

# 启动线程的类
class Thread_transform_json_to_txt(QThread):
    my_send_message = pyqtSignal(str, str)
    my_send_process_bar_message = pyqtSignal(int)
    my_send_dict_for_graph = pyqtSignal(dict)

    # 务必不要忘记set!!!
    def set_args(self, json_file_path: str, out_put_dir: str, moudle_name: str):
        self.json_file_path = json_file_path
        self.out_put_dir = out_put_dir
        self.moudle_name = moudle_name

    def my_sender(self, message: str, end='\n'):
        self.my_send_message.emit(message, end)

    def send_process(self, proc: int):
        self.my_send_process_bar_message.emit(proc)

    def send_dict_for_graph(self, my_dict: dict):
        self.my_send_dict_for_graph.emit(my_dict)

    def run(self):
        global g_sum_dict
        g_sum_dict = {}
        if running_state.is_running is False:
            running_state.is_running = True
            running_state.running_message = "生成工作空间"
            main_run(json_file_path=self.json_file_path, out_put_dir=self.out_put_dir, moudle_name=self.moudle_name)
            running_state.is_running = False
        else:
            print("程序正在进行%s, 结束前不要进行其他操作！" % running_state.running_message)
            self.my_send_message("程序正在进行%s, 结束前不要进行其他操作！" % running_state.running_message)
            self.exit(0)


thread_transform_json_to_txt = Thread_transform_json_to_txt()
