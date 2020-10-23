from analysis.AnaStruct import Num, WeiBo
import os, sys


def get_threshold():
    """
    将阀值数值写入配置文件

    这个函数可以读取该文件并返回阀值

    :return: 一个int，内容是阀值
    """
    if os.path.isfile("threshold.ini") is False:
        with open('threshold.ini', 'w+', encoding='utf-8') as f:
            f.write("3")
        return 3.0
    else:
        with open('threshold.ini', 'r', encoding='utf-8') as f:
            a = f.readline().replace('\n', '')
        return float(a)


def calc_present(big: int, small: int):
    """
    计算small占big的百分之多少
    """
    if big == 0:
        print("error big=%d, small=%d" % (big, small))
        return -1
    return small / big


def calc(num: Num):
    """
    这种分析方法的参考来源是《Sentiment Analysis on Naija-Tweets》
    """
    threshold = get_threshold()  # 计算阀值，默认值为 3，更改配置文件来改变阈值
    weibo = WeiBo()
    # 得分后的乘的数，是可以更改的。
    P_modification = num.ppnum_modification + (num.pqnum_modification * 1.1)  # 正向得分
    N_modification = num.npnum_modification + (num.nqnum_modification * 1.1)  # 负面得分
    # 言辞激烈程度得分
    # 程度等级的词汇的个数
    # most  程度最强烈       得分 3
    # very  程度较强烈       得分    2
    # more  程度比较强烈      得分   1
    # ish   程度稍微强烈      得分   -1
    # insufficiently  程度欠强烈  得分 -2
    # over 程度不强烈            得分 -3

    # 程度词修正(指数权值)
    most = (1 + 0.3) ** num.mostNum
    very = (1 + 0.2) ** num.veryNum
    more = (1 + 0.1) ** num.moreNum
    ish = (1 - 0.1) ** num.ishNum
    insufficiently = (1 - 0.2) ** num.insNum
    over = (1 - 0.3) ** num.overNum

    b = most * very * more * ish * insufficiently * over

    weibo.P_modification = P_modification * b
    weibo.N_modification = N_modification * b
    weibo.P_enum = 0
    weibo.I_enum = 0
    weibo.N_enum = 0
    weibo.none_enum = 0

    if P_modification > threshold and N_modification > threshold:
        weibo.I_enum = 1
    elif (P_modification < threshold and N_modification < threshold) or P_modification == N_modification:
        weibo.none_enum = 1
    elif P_modification > N_modification and ((P_modification > threshold > N_modification) or (
            P_modification < threshold < N_modification)):
        weibo.P_enum = 1
    else:
        weibo.N_enum = 1

    return weibo
