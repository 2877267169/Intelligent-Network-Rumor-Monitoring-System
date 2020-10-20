import time
import json, os
from data import data_ops
import LAC

from analysis.file_tools import division, participle

# data = data_ops.Data_ops(r"E:\py\test_dataset")
from analysis.sentiment_count import statistics
from analysis.AnaStruct import Num, WeiBo
from analysis.calculation import calc
from analysis.time_processer import show_time
from analysis import analysis_processer

lac = LAC.LAC()


def start(work_path: str):
    P_modification = {}
    N_modification = {}
    num = Num()
    weibo = WeiBo()
    data = data_ops.Data_ops(work_path)
    path = data.get_all_path()
    if len(path) == 0:
        return

    start_t = time.time()
    cnt = 0
    for i in range(len(path)):

        if len(path[i]) == 0:
            return
        p = division(path[i])
        if len(p[3]) == 0:
            p[3] += " "
        l = participle(p[3])

        num = statistics(l[0])

        weibo = calc(num)

        # print(weibo.P_modification)
        # print("--------------------")
        # print(weibo.N_modification)
        if p[0] in P_modification.keys():
            P_modification[p[0]] += weibo.P_modification
        if p[0] not in P_modification.keys():
            P_modification[p[0]] = weibo.P_modification
        if p[0] in N_modification.keys():
            N_modification[p[0]] += weibo.N_modification
        if p[0] not in N_modification.keys():
            N_modification[p[0]] = weibo.N_modification
        if cnt % 51 == 0:
            show_time(start_t=start_t, p=(cnt / len(path)))
            analysis_processer.analise_message.f_send_my_analyse_process_bar(int((cnt / len(path)) * 100))
        cnt += 1

    print(P_modification)
    print(N_modification)

    P_obj = {
        "date": list(P_modification.keys()),
        "data": list(P_modification.values())
    }

    N_obj = {
        "date": list(N_modification.keys()),
        "data": list(N_modification.values())
    }

    with open(os.path.join(work_path, "P.json"), 'w+', encoding='utf-8') as f:
        json.dump(P_obj, f, ensure_ascii=False)

    with open(os.path.join(work_path, "N.json"), 'w+', encoding='utf-8') as f:
        json.dump(N_obj, f, ensure_ascii=False)
    pass


if __name__ == '__main__':
    start(r"E:\py\test_dataset")
