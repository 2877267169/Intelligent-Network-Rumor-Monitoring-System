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
from analysis import file_tools

lac = LAC.LAC()


def start(work_path: str):
    P_modification = {}
    N_modification = {}

    none_enum = {}
    I_enum = {}

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
        # 负向的微博
        if weibo.N_enum == 1 and weibo.P_enum == 0 and weibo.none_enum == 0 and weibo.I_enum == 0:
            if p[0] in N_modification.keys():
                N_modification[p[0]] += weibo.N_enum
            if p[0] not in N_modification.keys():
                N_modification[p[0]] = weibo.N_enum
        # 正向的微博
        if weibo.N_enum == 0 and weibo.P_enum == 1 and weibo.none_enum == 0 and weibo.I_enum == 0:
            if p[0] in P_modification.keys():
                P_modification[p[0]] += weibo.P_enum
            if p[0] not in P_modification.keys():
                P_modification[p[0]] = weibo.P_enum
        # 言辞比较激烈的微博
        if weibo.N_enum == 0 and weibo.P_enum == 0 and weibo.none_enum == 0 and weibo.I_enum == 1:
            if p[0] in I_enum.keys():
                I_enum[p[0]] += weibo.I_enum
            if p[0] not in I_enum.keys():
                I_enum[p[0]] = weibo.I_enum
        # 什么也不是的微博
        if weibo.N_enum == 0 and weibo.P_enum == 0 and weibo.none_enum == 1 and weibo.I_enum == 0:
            if p[0] in none_enum.keys():
                none_enum[p[0]] += weibo.none_enum
            if p[0] not in none_enum.keys():
                none_enum[p[0]] = weibo.none_enum

        # print(weibo.P_modification)
        # print("--------------------")
        # print(weibo.N_modification)
        # 根据日期写字典

        if cnt % 51 == 0:
            show_time(start_t=start_t, p=(cnt / len(path)))
        cnt += 1

    with open(os.path.join(work_path, "P.json"), 'w+', encoding='utf-8') as f:
        json.dump(
            file_tools.transformer_direction(P_modification),
            f, ensure_ascii=False
        )

    with open(os.path.join(work_path, "N.json"), 'w+', encoding='utf-8') as f:
        json.dump(
            file_tools.transformer_direction(N_modification),
            f, ensure_ascii=False
        )
    with open(os.path.join(work_path, "I.json"), 'w+', encoding='utf-8') as f:
        json.dump(
            file_tools.transformer_direction(I_enum),
            f, ensure_ascii=False)
    with open(os.path.join(work_path, "none.json"), 'w+', encoding='utf-8') as f:
        json.dump(
            file_tools.transformer_direction(none_enum),
            f, ensure_ascii=False
        )


if __name__ == '__main__':
    start(r"E:\py\test_dataset")
