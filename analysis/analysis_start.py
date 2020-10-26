import time
import json, os

from analysis.percentage import percentage
from data import data_ops

from analysis.file_tools import division, participle

# data = data_ops.Data_ops(r"E:\py\test_dataset")
from analysis.sentiment_count import statistics
from analysis.AnaStruct import Num, WeiBo
from analysis.calculation import calc
from analysis.time_processer import show_time
from analysis import analysis_processer
from analysis import file_tools


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

    P_keys = list(P_modification.keys())
    N_keys = list(N_modification.keys())
    I_keys = list(I_enum.keys())
    none_keys = list(none_enum.keys())
    # print("hsgdfhjsd gjf sdghjfgsdhjfsdhjfgSDHJFGASDHJFGHJSDFGHMSDGFHJKSDGFJKGSDKFGHSDJKFGKSDHJG")
    # print(P_keys[2])

    # P I 互补日期
    for i in P_keys:
        if i not in I_keys:
            I_enum[i] = 0
    for i in I_keys:
        if i not in P_keys:
            P_modification[i] = 0
    # N none 互补日期
    for i in N_keys:
        if i not in none_keys:
            none_enum[i] = 0
    for i in none_keys:
        if i not in N_keys:
            N_modification[i] = 0
    # 刷新键值
    P_keys = list(P_modification.keys())
    N_keys = list(N_modification.keys())
    I_keys = list(I_enum.keys())
    none_keys = list(none_enum.keys())

    # PN互补日期
    for i in P_keys:
        if i not in N_keys:
            N_modification[i] = 0
    for i in N_keys:
        if i not in P_keys:
            P_modification[i] = 0
    # I none互补日期
    for i in I_keys:
        if i not in none_keys:
            none_enum[i] = 0
    for i in none_keys:
        if i not in I_keys:
            I_enum[i] = 0
    total = percentage(P_modification, N_modification, I_enum, none_enum)

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
    # 将生成的百分比字典携程json文件
    # 正向在一天中所占的百分比
    with open(os.path.join(work_path, "P_percentage.json"), 'w+', encoding='utf-8') as f:
        json.dump(
            file_tools.transformer_direction(total[0]),
            f, ensure_ascii=False
        )
    # 负向在一天中所占的比例
    with open(os.path.join(work_path, "N_percentage.json"), 'w+', encoding='utf-8') as f:
        json.dump(
            file_tools.transformer_direction(total[1]),
            f, ensure_ascii=False
        )
    # 激烈在一天中所占的百分比
    with open(os.path.join(work_path, "I_percentage.json"), 'w+', encoding='utf-8') as f:
        json.dump(
            file_tools.transformer_direction(total[2]),
            f, ensure_ascii=False
        )
    # none类型在一天中所占的比例

    with open(os.path.join(work_path, "none_percentage.json"), 'w+', encoding='utf-8') as f:
        json.dump(
            file_tools.transformer_direction(total[3]),
            f, ensure_ascii=False
        )


if __name__ == '__main__':
    start(r"E:\py\test_dataset")
