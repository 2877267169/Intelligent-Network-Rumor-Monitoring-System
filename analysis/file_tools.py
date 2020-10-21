from data import data_ops
import LAC
import set_page_corpus_connect
import os, sys

data = data_ops.Data_ops(r"E:\py\test_dataset")
lac = LAC.LAC()


def transformer_direction(my_dict_obj:dict):
    r = {
        "date": list(my_dict_obj.keys()),
        "data": list(my_dict_obj.values())
    }
    return r


# 获取评价和情感的列表
def getSentiment():
    """

    :return: 获取评价和情感的列表
    """

    cps_from_ui = set_page_corpus_connect.get_all_path()
    sentiment_base_dir = cps_from_ui[set_page_corpus_connect.path_para.dict]

    list_of_sentiment = []
    # 修改文件名称
    path = [
        # r"E:\py\sentiment\负面评价词语（中文）.txt",
        os.path.join(sentiment_base_dir, "负面评价词语（中文）_utf_8.txt"),
        # r"E:\py\sentiment\负面情感词语（中文）.txt",
        os.path.join(sentiment_base_dir, "负面情感词语（中文）_utf_8.txt"),
        # r"E:\py\sentiment\正面评价词语（中文）.txt",
        os.path.join(sentiment_base_dir, "正面评价词语（中文）_utf_8.txt"),
        # r"E:\py\sentiment\正面情感词语（中文）.txt"
        os.path.join(sentiment_base_dir, "正面情感词语（中文）_utf_8.txt")
    ]
    for i in range(4):
        with open(path[i], "r", encoding="utf-8") as f:

            if f == None:
                return
            l = f.readlines()
            if l == None:
                return
            for j in range(len(l)):
                l[j] = l[j][:-2]

            list_of_sentiment.append(l)
            # list_of_sentiment[0]是  负面评价词语
            # list_of_sentiment[1]是负面情感词语
            # list_of_sentiment[2]是正面评价词
            # list_of_sentiment[3]是正面情感词

    return list_of_sentiment


# 程度级别词语分为六类，每一个类有相应的得分
def getDegree():
    """
    # most 程度最强烈            得分  6\n
    # very  程度较强烈           得分  5\n
    # more  程度比较强烈         得分   4\n
    # ish   程度稍微强烈         得分   3\n
    # insufficiently 程度欠强烈  得分  2\n
    # over 程度不强烈            得分  1\n
    :return: 程度级别词分词后存放到 degree列表中\n
    """
    cps_from_ui = set_page_corpus_connect.get_all_path()
    sentiment_base_dir = cps_from_ui[set_page_corpus_connect.path_para.dict]

    degree = []
    path = [
        os.path.join(sentiment_base_dir, "most.txt",),
        os.path.join(sentiment_base_dir, "very.txt"),
        os.path.join(sentiment_base_dir, "more.txt"),
        os.path.join(sentiment_base_dir, "ish.txt"),
        os.path.join(sentiment_base_dir, "insufficiently.txt"),
        os.path.join(sentiment_base_dir, "over.txt")
    ]
    for i in range(6):
        with open(path[i], "r", encoding="utf-8") as f:
            l = f.readlines()
            if l == None:
                return
            for j in range(len(l)):
                l[j] = l[j][:-1]

        degree.append(l)
    #  print(degree)

    return degree


def division(path):
    """
    对文本文件进行分割，division→分割  接收的参数是文件的路径\n
    得到日期和文本内容、\n
    p[0] 字符串日期\n
    中间是无关信息\n
    p[3] 字符串文本\n
    """
    if len(path) == 0:
        return
    p = data.get_file_text(path).split("\t")
    if len(p) == 0:
        return
    return p


def participle(test):
    """
    对文本进行分词participle→分词 参数为字符串文本。\n
    :return: 分词后的列表
    """
    if len(test) == 0:
        test += " "
    l = lac.run(test)
    if len(l) == 0:
        l += " "
    return l


if __name__ == '__main__':
    # p= getqinggan()
    # print(p[0])
    # main()
    # getDegree()

    l = participle("山东冠县女子被人顶替上大学：我就想知道她是怎么拿到我的通知书的。调查进行中，愿能还给她迟到的真相！#顶替他人上大学女子成绩低于分数线243分#@人民日报")
    print(l)
