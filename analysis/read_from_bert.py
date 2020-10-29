# from analysis import file_tools
from data import data_ops
import json, os


def read(work_path: str):
    # 是谣言概率
    is_rumor = {}
    # 不是谣言概率
    not_is_rumor = {}
    # 同一天的微博数量
    weibo_num = {}

    global my_data
    my_data = data_ops.Data_ops(work_path)
    path = my_data.get_all_path()
    date = []
    # 是谣言的概率数组
    is_Rumor_probability = []
    # 不是谣言的概率数组
    not_is_Rumor_probability = []
    # for i in path :
    #     p =division(i)
    #     #日期
    #     date.append(p)
    # 读取test_results.tsv
    f = open(r"E:\py\test_results.tsv", "r", encoding="utf-8")

    probability = f.readlines()
    for i in probability:
        d = i.split("\t")

        is_Rumor_probability.append(float(d[0]))
        not_is_Rumor_probability.append(float(d[1][:-1]))

    # 读取weibo，获取日期
    for i in path:
        d = open(i, "r", encoding="utf-8")

        date.append(d.read().split("\t")[0])
    d.close()
    # 获取同一天微博的数量
    for i in date:
        if i in weibo_num.keys():
            weibo_num[i] += 1
        if i not in weibo_num.keys():
            weibo_num[i] = 1

    # 获取同一天的微博的是谣言概率的和。
    for i in range(len(is_Rumor_probability)):
        if date[i] in is_rumor.keys():
            is_rumor[date[i]] += 1.0 * is_Rumor_probability[i]
        if date[i] not in is_rumor.keys():
            is_rumor[date[i]] = 1.0 * is_Rumor_probability[i]
    for i in range(len(not_is_Rumor_probability)):
        if date[i] in not_is_rumor.keys():
            not_is_rumor[date[i]] += 1.0 * not_is_Rumor_probability[i]
        if date[i] not in not_is_rumor.keys():
            not_is_rumor[date[i]] = 1.0 * not_is_Rumor_probability[i]
    for i in is_rumor.keys():
        is_rumor[i] = is_rumor[i] / weibo_num[i]
    for i in not_is_rumor.keys():
        not_is_rumor[i] = not_is_rumor[i] / weibo_num[i]
    f.close()


def get_bert_res_to_json(work_path: str, bert_train_res_file_path: str):
    """

    :param bert_train_res_file_path:BERT 训练文件结果
    :param work_path:工作目录：用于获取路径（路径用于获取日期）
    :return:None
    """
    # 将日期列表、是谣言概率的列表和不是谣言概率的列表 存放到这个总的列表中
    total = []
    my_data = data_ops.Data_ops(work_path)
    path = my_data.get_all_path()
    # 存放日期的列表
    date = []
    # 是谣言概率
    is_Rumor_probability = []
    # 不是谣言概率
    not_is_Rumor_probability = []
    if len(path) == 0:
        return 0

    # 处理TSV文件
    with open(bert_train_res_file_path, "r", encoding="utf-8") as f:
        probability = f.readlines()
        for i in probability:
            d = i.split("\t")

            is_Rumor_probability.append(float(d[0]))
            not_is_Rumor_probability.append(float(d[1][:-1]))
    # 读取weibo，获取日期
    for i in range(len(probability)):
        with open(path[i], "r", encoding="utf-8") as d:
            date.append(d.read().split("\t")[0])

    total.append(date)
    total.append(is_Rumor_probability)
    total.append(not_is_Rumor_probability)
    print(len(total))
    print(len(date))
    print(len(is_Rumor_probability))
    print(len(not_is_Rumor_probability))
    with open(os.path.join(work_path, "toal.json"), 'w+', encoding='utf-8') as f:
        json.dump(total, f, indent=4)

# if __name__ == '__main__':
#     # read(r"E:\py\test_dataset")
#     get_bert(r"E:\py\test_dataset")
