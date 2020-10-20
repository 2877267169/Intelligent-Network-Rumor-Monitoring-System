class Num:
    """
    定义nun类。用于参数的传递
    记录情感词频率
    PP: Positive Pingjia
    PQ: Positive Qinggan
    NP: Negative Pingjia
    NQ: Negative Qinggan

    # 其余为程度逐级递减的情感词
    """

    def __init__(self):
        self.ppnum_modification = 0  # 正面评价词的个数
        self.pqnum_modification = 0  # 正面情感词的个数
        self.npnum_modification = 0  # 负面评价词的个数
        self.nqnum_modification = 0  # 负面情感词的个数

        self.mostNum = 0
        self.veryNum = 0
        self.moreNum = 0
        self.ishNum = 0
        self.insNum = 0
        self.overNum = 0


class WeiBo:
    """
    微博的属性
    N_modification:积极记录
    P_modification:消极情感记录
    """
    def __init__(self):
        self.P_modification = 0
        self.N_modification = 0
