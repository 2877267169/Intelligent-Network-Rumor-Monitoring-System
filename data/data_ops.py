"""
数据集读取工具 版本 1.0

"""
import os


# 有关数据集的操作
class Data_ops:

    def __init__(self, index_data: str):
        self.data_index_dir = index_data.replace('"', '')
        self.reply_index_dir = os.path.join(self.data_index_dir, 'reply')
        self.data_index = os.path.join(index_data, 'index.txt')

    # 测试数据集完整性
    def test(self):
        return os.path.isdir(self.data_index_dir) and \
               os.path.isfile(self.data_index) and \
               os.path.isdir(self.reply_index_dir)

    # 加载所有的微博文件名（不包括路径）
    def load_index_file_name(self):
        r = []
        with open(self.data_index, 'r', encoding='utf-8') as f:
            while True:
                file_name = f.readline().replace('\n', '')
                if file_name == '':
                    break
                r.append(file_name)
        return r

    # 加载所有的微博文件名（包括路径）
    def load_index_file_path(self):
        l = self.load_index_file_name()
        for i in range(len(l)):
            l[i] = os.path.join(self.data_index_dir, l[i])
        return l

    # 加载所有的微博回复文件夹（包括路径）
    def load_reply_dir(self):
        l = self.load_index_file_name()
        for i in range(len(l)):
            l[i] = os.path.join(self.data_index_dir, 'reply', l[i][:-4])  # 去掉 .txt
        return l

    # 根据回复文件夹路径，获取回复列表(包括路径)
    def load_reply_file_path(self, reply_dir: str):
        index_file_path = os.path.join(self.reply_index_dir, reply_dir)
        with open(os.path.join(index_file_path, 'reply_index.txt')) as f:
            file_names = f.readlines()
        for i in range(len(file_names)):
            file_names[i] = os.path.join(index_file_path, file_names[i].replace('\n', ''))
        return file_names

    # 遍历所有的文件
    def get_all_path(self):
        rep_dir = self.load_reply_dir()
        res = self.load_index_file_path()

        for i in range(len(res) - 1, 0 - 1, -1):  # 倒序遍历
            n = self.load_reply_file_path(reply_dir=rep_dir[i])
            for nn in n:
                res.insert(i + 1, nn)
        return res

    # 获得文件的内容
    def get_file_text(self, file_path: str):
        with open(file_path, 'r', encoding='utf-8') as f:
            l = f.readlines()
        res = ""
        for s in l:
            res += s
        return res

    def get_file_raw_text(self, file_path: str):
        with open(file_path, 'r', encoding='utf-8') as f:
            l = f.readlines()
        res = ""
        for s in l:
            res += s
        return res

    def transforme_to_mark_file_path(self, base_dir: str, file_path_list: list):
        for i in range(len(file_path_list)):
            print(base_dir)
            print(file_path_list[i])
            file_path_list[i] = file_path_list[i].replace(base_dir, os.path.join(base_dir, 'mark/'))
        return file_path_list
