import json
import os

import numpy as np


def calc_var(my_list: list):
    """
    计算方差（即标准差的平方）\n 方差揭示了数据的波动情况
    :param my_list:  输入数组
    :return: 标准差
    """
    return float(np.var(my_list))


def calc_a_E(my_list: list):
    """
    获取增长率的均值

    :param my_list:  输入数组
    :return: 增长率的均值
    """
    cnt = 0
    for i in range(1, len(my_list)):
        cnt += my_list[i] - my_list[i - 1]
    cnt /= len(my_list)
    return cnt


def put_level(num: float, num_list_for_level=None, str_list_for_description=None):
    if str_list_for_description is None:
        str_list_for_description = [
            "环境平稳",
            "有所异见",
            "异见较多",
            "剧烈异见"
        ]
    if num_list_for_level is None:
        num_list_for_level = [0, 0.3, 0.5, 0.7, 1]
    while len(str_list_for_description) < len(num_list_for_level) - 1:
        str_list_for_description.append("no define")

    for i in range(1, len(num_list_for_level)):
        if num_list_for_level[i - 1] < num <= num_list_for_level[i]:
            return str_list_for_description[i - 1]
    return "err"


def warning_start(n: list, i: list, work_path: str):
    warning_cnt = 0

    n_var = calc_var(my_list=n)
    n_a_e = calc_a_E(my_list=n)
    if n_var > 0.5:
        warning_cnt += 1
    if n_a_e > 0.5:
        warning_cnt += 1

    i_var = calc_var(my_list=i)
    i_a_e = calc_a_E(my_list=i)

    if i_var > 0.5:
        warning_cnt += 1
    if i_a_e > 0.5:
        warning_cnt += 1

    n_var_desc = put_level(num=n_var)
    n_a_e_desc = put_level(
        num=n_a_e,
        num_list_for_level=[-2, -0.5, -0.25,0.25, 0.5, 2],
        str_list_for_description=[
            "剧烈减少",
            "减少",
            "波动平稳",
            "增加",
            "剧烈增加"
        ]
    )

    i_var_desc = put_level(num=i_var)
    i_a_e_desc = put_level(
        num=i_a_e,
        num_list_for_level=[-2, -0.5, -0.25,0.25, 0.5, 2],
        str_list_for_description=[
            "剧烈减少",
            "减少",
            "波动平稳",
            "增加",
            "剧烈增加"
        ]
    )

    res = ["安全", "注意", "警告", "特别警告", "危险"]
    out_obj = [
        [n_var, n_var_desc],
        [n_a_e, n_a_e_desc],
        [i_var, i_var_desc],
        [i_a_e, i_a_e_desc],
        [warning_cnt, res[warning_cnt]]
    ]
    with open(os.path.join(work_path, "warning.json"), "w+", encoding="utf-8") as f:
        json.dump(out_obj, f, indent=4, ensure_ascii=False)


def get_obj(work_path: str):
    with open(os.path.join(work_path, "warning.json"), "r", encoding="utf-8") as f:
        my_obj = json.load(f)

    return my_obj
