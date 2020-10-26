from analysis.file_tools import getSentiment, getDegree
import time

# 接收的参数   l   分词之后的列表
from analysis.AnaStruct import Num


def statistics(l: list):
    """
         Statistics   统计词在各个分类下的个数
    :param l: 分词之后的列表
    :return: 参数列表。num数组
    """
    # n 接收情感的参数列表
    # d 接收程度等级词汇列表
    # npnum_modification 负面评价词的个数

    if len(l) == 0:
        l += " "
    npnum_modification = 0
    # npnum_modification 负面情感词的个数
    nqnum_modification = 0
    # ppnum_modification 正面评价词的个数
    ppnum_modification = 0
    # pqnum_modification 正面情感词的个数
    pqnum_modification = 0

    # 程度等级的词汇的个数
    # most 程度最强烈  得分 6
    # very  程度较强烈    得分    5
    # more  程度比较强烈    得分   4
    # ish   程度稍微强烈    得分   3
    # insufficiently 程度欠强烈  得分 2
    # over 程度不强烈            得分 1
    mostNum = 0
    veryNum = 0
    moreNum = 0
    ishNum = 0
    insNum = 0
    overNum = 0
    list_of_sentiment = getSentiment()
    # print(list_of_sentiment[0])
    # print(list_of_sentiment[1])
    # print(list_of_sentiment[2])
    # print(list_of_sentiment[3])
    d = getDegree()
    # list_of_sentiment[0]是  负面评价词语
    # list_of_sentiment[1]是负面情感词语
    # list_of_sentiment[2]是正面评价词
    # list_of_sentiment[3]是正面情感词

    for i in range(len(l)):
        if l[i] in list_of_sentiment[0]:
            npnum_modification += 1
        if l[i] in list_of_sentiment[1]:
            nqnum_modification += 1
        if l[i] in list_of_sentiment[2]:
            ppnum_modification += 1
        if l[i] in list_of_sentiment[3]:
            pqnum_modification += 1
        """if l[i] in d[0]:
            mostNum += 1
        if l[i] in d[1]:
            veryNum += 1
        if l[i] in d[2]:
            moreNum += 1
        if l[i] in d[3]:
            ishNum += 1
        if l[i] in d[4]:
            insNum += 1
        if l[i] in d[5]:
            overNum += 1"""

    num = Num()
    num.npnum_modification = npnum_modification
    num.nqnum_modification = nqnum_modification
    num.ppnum_modification = ppnum_modification
    num.pqnum_modification = pqnum_modification
    num.mostNum = mostNum
    num.veryNum = veryNum
    num.moreNum = moreNum
    num.ishNum = ishNum
    num.insNum = insNum
    num.overNum = overNum

    return num


if __name__ == '__main__':
    # calc(['山东', '冠县', '女子', '被', '人', '顶替', '上', '大学', '：', '我', '就', '想知道', '她', '是', '怎么', '拿到', '我', '的', '通知书',
    # '的', '。', '调查', '进行', '中', '，', '愿', '能', '还给', '她', '迟到', '的', '真相', '！', '#', '顶替', '他人', '上', '大学', '女子',
    # '成绩', '低于', '分数线', '243分', '#@人民日报'])
    statistics(['距离', '孔子', '的', '老家', '也', '就', '30公里', '的', '样子', '，', '孔孟', '之', '乡', '，', '礼仪之邦'])
