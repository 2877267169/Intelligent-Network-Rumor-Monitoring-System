from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QLineEdit, QPushButton, QMessageBox
import os, sys
import set_page_corpus_connect
from bert import run_classifier
from bert import run_test
import MainWindow
from data import transform_json_to_txt
from data import bert_train_complex
import running_state
import json

# matplotlib 和qt链接的包
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

# is_run_available = False

my_ui = MainWindow.Ui_MainWindow()
is_accept = False


# 定义字典的参数，防止以后输错
class TrainParameters:

    def __init__(self):
        self.do_lower_case = "do_lower_case"
        self.max_seq_length = "max_seq_length"
        self.do_train = "do_train"
        self.do_eval = "do_eval"
        self.do_predict = "do_predict"
        self.train_batch_size = "train_batch_size"
        self.eval_batch_size = "eval_batch_size"
        self.predict_batch_size = "predict_batch_size"
        self.learning_rate = "learning_rate"
        self.num_train_epochs = "num_train_epochs"
        self.warmup_proportion = "warmup_proportion"
        self.save_checkpoints_steps = "save_checkpoints_steps"
        self.use_tpu = "use_tpu"


class FileParameters():
    def __init__(self):
        self.data_dir = 'data_dir'
        self.bert_config_file = 'bert_config_file'
        self.vocab_file = 'vocab_file'
        self.output_dir = 'output_dir'
        self.init_checkpoint = 'init_checkpoint'


train_parameters = TrainParameters()
file_parameters = FileParameters()


def set_page_train_connect(ui: MainWindow.Ui_MainWindow):
    global pie_ax
    global my_ui
    global FC_train
    my_ui = ui

    # 按钮
    my_ui.my_page_train_button_data_dir.clicked.connect(get_user_input_and_set_to_data_dir)
    my_ui.my_page_train_button_bert_config_file.clicked.connect(get_user_input_and_set_to_bert_config_file)
    my_ui.my_page_train_button_vocab_file.clicked.connect(get_user_input_and_set_to_vocab_file)
    my_ui.my_page_train_button_output_dir.clicked.connect(get_user_input_and_set_to_output_dir)
    my_ui.my_page_train_button_init_checkpoint.clicked.connect(get_user_input_and_set_to_init_checkpoint)

    # 设为默认的按钮
    my_ui.my_page_train_tp_pushButtton_clear_and_set_to_default.clicked.connect(set_all_training_parameters_default)

    # 命令按钮
    my_ui.my_page_train_commandLinkButton_verify.clicked.connect(verify)
    my_ui.my_page_train_commandLinkButton_run.clicked.connect(run_for_bert)

    # 将参数设为默认
    set_all_training_parameters_default(is_message=False)

    # 大画板！！！！！
    train_f = plt.figure()
    FC_train = FigureCanvas(train_f)
    # 将大画板插入组件！！！
    my_ui.my_page_train_gridLayout_graph.layout().addWidget(FC_train)

    # pie_ax就是我要画饼的组件了！！
    pie_ax = train_f.add_subplot('111')

    pie_ax.cla()
    pie_ax.set_title('The Predict Result of BERT Training')

    draw_pie([100], ['waiting for analyze'])

    #draw_pie()

    # 读取上一次的配置
    if os.path.isfile('file_para.json') is True:
        print('检测到配置文件, 现在加载')
        with open('file_para.json', 'r+', encoding='utf-8') as f:
            json_file_para = json.load(f)
            my_ui.my_page_train_lineEdit_data_dir.setText(json_file_para[file_parameters.data_dir])
            my_ui.my_page_train_lineEdit_bert_config_file.setText(json_file_para[file_parameters.bert_config_file])
            my_ui.my_page_train_lineEdit_vocab_file.setText(json_file_para[file_parameters.vocab_file])
            my_ui.my_page_train_lineEdit_output_dir.setText(json_file_para[file_parameters.output_dir])
            my_ui.my_page_train_lineEdit_init_checkpoint.setText(json_file_para[file_parameters.init_checkpoint])


def get_user_input_and_set_to_data_dir():
    global my_ui
    data_dir = QFileDialog.getExistingDirectory(my_ui.my_page_train_lineEdit_data_dir, 'open for data dir:', '.')
    my_ui.my_page_train_lineEdit_data_dir.setText(data_dir)


def get_user_input_and_set_to_bert_config_file():
    global my_ui
    bert_config_file, _ = QFileDialog.getOpenFileName(my_ui.my_page_train_lineEdit_bert_config_file,
                                                      'open for bert config file', '.', "bert config file(*.json)")
    my_ui.my_page_train_lineEdit_bert_config_file.setText(bert_config_file)


def get_user_input_and_set_to_vocab_file():
    global my_ui
    vocab_file, _ = QFileDialog.getOpenFileName(my_ui.my_page_train_lineEdit_vocab_file,
                                                'open for vocab file', '.', "vocab file(vocab.txt)")
    my_ui.my_page_train_lineEdit_vocab_file.setText(vocab_file)


def get_user_input_and_set_to_output_dir():
    global my_ui
    output_dir = QFileDialog.getExistingDirectory(my_ui.my_page_train_lineEdit_output_dir, 'open for output dir',
                                                  '.')
    my_ui.my_page_train_lineEdit_output_dir.setText(output_dir)


def get_user_input_and_set_to_init_checkpoint():
    global my_ui
    init_checkpoint, _ = QFileDialog.getOpenFileName(my_ui.my_page_train_lineEdit_init_checkpoint,
                                                     'open for init checkpoint file', '.',
                                                     "init checkpoint file(*.ckpt.index)")
    # 替换， 因为原模型有这样一个细节，ckpt文件实际有三个部分组成，传参数只传一个ckpt之前文件名，看看文件结构就知道了
    # 替换， 因为原模型有这样一个细节，ckpt文件实际有三个部分组成，传参数只传一个ckpt之前文件名，看看文件结构就知道了
    init_checkpoint = str(init_checkpoint).replace('.index', '')
    my_ui.my_page_train_lineEdit_init_checkpoint.setText(init_checkpoint)


def get_all_file_parameters():
    global my_ui
    return {
        file_parameters.data_dir: my_ui.my_page_train_lineEdit_data_dir.text(),
        file_parameters.bert_config_file: my_ui.my_page_train_lineEdit_bert_config_file.text(),
        file_parameters.vocab_file: my_ui.my_page_train_lineEdit_vocab_file.text(),
        file_parameters.output_dir: my_ui.my_page_train_lineEdit_output_dir.text(),
        file_parameters.init_checkpoint: my_ui.my_page_train_lineEdit_init_checkpoint.text()
    }


def get_all_training_parameters():
    global my_ui
    global train_parameters
    return {
        train_parameters.do_lower_case: my_ui.my_page_train_tp_comboBox_do_lower_case.currentText(),
        train_parameters.max_seq_length: my_ui.my_page_train_tp_spinBox_max_seq_length.value(),
        train_parameters.do_train: my_ui.my_page_train_tp_comboBox_do_train.currentText(),
        train_parameters.do_eval: my_ui.my_page_train_tp_comboBox_do_eval.currentText(),
        train_parameters.do_predict: my_ui.my_page_train_tp_comboBox_do_predict.currentText(),
        train_parameters.train_batch_size: my_ui.my_page_train_tp_spinBox_train_batch_size.value(),
        train_parameters.eval_batch_size: my_ui.my_page_train_tp_spinBox_eval_batch_size.value(),
        train_parameters.predict_batch_size: my_ui.my_page_train_tp_spinBox_predict_batch_size.value(),
        train_parameters.learning_rate: my_ui.my_page_train_tp_lineEdit_learning_rate.text(),
        train_parameters.num_train_epochs: my_ui.my_page_train_tp_doubleSpinBox_num_train_epochs.value(),
        train_parameters.warmup_proportion: my_ui.my_page_train_tp_doubleSpinBox_warmup_proportion.value(),
        train_parameters.save_checkpoints_steps: my_ui.my_page_train_tp_spinBox_save_checkpoints_steps.value(),
        train_parameters.use_tpu: my_ui.my_page_train_tp_comboBox_use_tpu.currentText(),
    }


def set_all_training_parameters_default(is_message=True):
    global my_ui
    if is_message is True:
        r = QMessageBox.question(my_ui.my_page_train_tp_pushButtton_clear_and_set_to_default, "警告", '你确定要重置参数为默认参数吗？',
                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if r == QMessageBox.No:
            return
    # 确认要重置

    my_ui.my_page_train_tp_comboBox_do_lower_case.setCurrentIndex(1)
    my_ui.my_page_train_tp_spinBox_max_seq_length.setValue(128)
    my_ui.my_page_train_tp_comboBox_do_train.setCurrentIndex(0)
    my_ui.my_page_train_tp_comboBox_do_eval.setCurrentIndex(0)
    my_ui.my_page_train_tp_comboBox_do_predict.setCurrentIndex(0)
    my_ui.my_page_train_tp_spinBox_train_batch_size.setValue(32)
    my_ui.my_page_train_tp_spinBox_eval_batch_size.setValue(8)
    my_ui.my_page_train_tp_spinBox_predict_batch_size.setValue(8)
    my_ui.my_page_train_tp_lineEdit_learning_rate.setText('5e-5')
    my_ui.my_page_train_tp_doubleSpinBox_num_train_epochs.setValue(3.0)
    my_ui.my_page_train_tp_doubleSpinBox_warmup_proportion.setValue(0.1)
    my_ui.my_page_train_tp_spinBox_save_checkpoints_steps.setValue(1000)
    my_ui.my_page_train_tp_comboBox_use_tpu.setCurrentIndex(0)


# 校验单个文件
def verify_files(file_name: str, description=''):
    global my_ui
    global is_accept
    if os.path.isfile(file_name) is False:
        is_accept = False
        QMessageBox.critical(my_ui.my_page_train,
                             '错误', '%s \n的路径存在问题。\n%s' % (file_name, description),
                             QMessageBox.Close)


def verify():
    global my_ui
    global is_accept
    global train_parameters
    file_parameters = get_all_file_parameters()
    training_parameters = get_all_training_parameters()
    is_accept = True
    if os.path.isdir(file_parameters['data_dir']) is False:
        is_accept = False
        QMessageBox.critical(my_ui.my_page_train, '错误', 'data_dir 的路径存在问题，请检查路径是否正确或是否有权限访问。', QMessageBox.Close)
    else:
        verify_files(os.path.join(file_parameters['data_dir'], 'bert_dev.tsv'),
                     description=' *请检查路径是否正确或是否有权限访问\n *请检查是否生成了训练文件')
        verify_files(os.path.join(file_parameters['data_dir'], 'bert_test.tsv'),
                     description=' *请检查路径是否正确或是否有权限访问\n *请检查是否生成了训练文件')
        verify_files(os.path.join(file_parameters['data_dir'], 'bert_train.tsv'),
                     description=' *请检查路径是否正确或是否有权限访问\n *请检查是否生成了训练文件')

    if os.path.isfile(file_parameters['bert_config_file']) is False:
        is_accept = False
        QMessageBox.critical(my_ui.my_page_train, '错误', 'bert_config_file 的路径存在问题，请检查路径是否正确或是否有权限访问。',
                             QMessageBox.Close)
    if os.path.isfile(file_parameters['vocab_file']) is False:
        is_accept = False
        QMessageBox.critical(my_ui.my_page_train, '错误', 'vocab_file 的路径存在问题，请检查路径是否正确或是否有权限访问。', QMessageBox.Close)
    if os.path.isdir(file_parameters['output_dir']) is False:
        is_accept = False
        QMessageBox.critical(my_ui.my_page_train, '错误', 'output_dir 的路径存在问题，请检查路径是否正确或是否有权限访问。', QMessageBox.Close)
    if os.path.isfile(file_parameters['init_checkpoint'] + '.index') is False:
        is_accept = False
        QMessageBox.critical(my_ui.my_page_train, '错误', 'init_checkpoint 的路径存在问题，请检查路径是否正确或是否有权限访问。',
                             QMessageBox.Close)

    if training_parameters['do_train'] == 'True':
        if set_page_corpus_connect.is_train_available is False:
            QMessageBox.critical(my_ui.my_page_train, '参数错误', 'do_train:\n  当前的数据集不能用于训练，请检查参数。',
                                 QMessageBox.Close)

    if training_parameters['do_predict'] == 'True':
        verify_files(os.path.join(file_parameters['output_dir'], 'train.tf_record'),
                     description='do_predict:\n  无法进行分析，因为没有进行训练或找不到模型文件')

    if is_accept is False:
        QMessageBox.critical(my_ui.my_page_train, '校验未通过', '校验未通过。',
                             QMessageBox.Close)
    else:
        QMessageBox.information(my_ui.my_page_train, "校验完成", "校验已成功完成，没有发现问题", QMessageBox.Ok)
        file_para = json.dumps(file_parameters, indent=4, ensure_ascii=False)
        with open('file_para.json', 'w+', encoding='utf-8') as f:
            f.write(file_para)
            print("保存了自定义配置")


def set_train_page_unable():
    global my_ui
    my_ui.my_page_train_tp_comboBox_do_lower_case.setDisabled(True)
    my_ui.my_page_train_tp_spinBox_max_seq_length.setDisabled(True)
    my_ui.my_page_train_tp_comboBox_do_train.setDisabled(True)
    my_ui.my_page_train_tp_comboBox_do_eval.setDisabled(True)
    my_ui.my_page_train_tp_comboBox_do_predict.setDisabled(True)
    my_ui.my_page_train_tp_spinBox_train_batch_size.setDisabled(True)
    my_ui.my_page_train_tp_spinBox_eval_batch_size.setDisabled(True)
    my_ui.my_page_train_tp_spinBox_predict_batch_size.setDisabled(True)
    my_ui.my_page_train_tp_lineEdit_learning_rate.setDisabled(True)
    my_ui.my_page_train_tp_doubleSpinBox_num_train_epochs.setDisabled(True)
    my_ui.my_page_train_tp_doubleSpinBox_warmup_proportion.setDisabled(True)
    my_ui.my_page_train_tp_spinBox_save_checkpoints_steps.setDisabled(True)
    my_ui.my_page_train_tp_comboBox_use_tpu.setDisabled(True)

    my_ui.my_page_train_button_data_dir.setDisabled(True)
    my_ui.my_page_train_button_bert_config_file.setDisabled(True)
    my_ui.my_page_train_button_vocab_file.setDisabled(True)
    my_ui.my_page_train_button_output_dir.setDisabled(True)
    my_ui.my_page_train_button_init_checkpoint.setDisabled(True)

    my_ui.my_page_train_commandLinkButton_verify.setDisabled(True)
    my_ui.my_page_train_commandLinkButton_run.setDisabled(True)


def run_for_bert():
    global is_accept
    global train_parameters
    global file_parameters

    my_file_parameters = get_all_file_parameters()
    if is_accept is False:
        QMessageBox.critical(my_ui.my_page_train, '校验未通过', '校验未通过, 无法启动。',
                             QMessageBox.Close)
        return
    else:
        if os.path.isfile(os.path.join(my_file_parameters[file_parameters.output_dir], 'test_results.tsv')) is True:
            res = QMessageBox.question(my_ui.my_page_train, "已有训练结果", "检测到你已经有了一个训练结果！是否现在分析？\n选择‘是’将会跳过训练，选择‘否’将仍然开始训练。",
                                 QMessageBox.Yes|QMessageBox.No, QMessageBox.Yes)
            if res == QMessageBox.No:
                pass# 继续训练！
            else:
                #选择是！！！！！
                read_and_set_pie()
                return

        my_training_parameters = get_all_training_parameters()
        warning = ''
        if my_training_parameters['do_train'] == 'True':
            warning += '* 你选择了训练模式，这将会需要一定时间（无GPU1-2小时，有GPU20分钟到1小时），\n'
        if my_training_parameters['do_eval'] == 'True':
            warning += '* 你选择了进行验证，这将会消耗一些时间并打印出现有模型的准确率。\n'
        if my_training_parameters['do_predict'] == 'True':
            warning += '* 你选择了进行分析，这将会把你的验证集数据送入模型并产出结果。\n'

        if warning == '':
            QMessageBox.critical(my_ui.my_page_train, '没有任务', '你没有选择执行任何任务！',
                                 QMessageBox.Close)
            return
        else:
            QMessageBox.warning(my_ui.my_page_train, "警告", warning, QMessageBox.Ok)
            r = QMessageBox.warning(
                my_ui.my_page_train, "警告——不可再次编辑!!",
                '一旦开始训练，不能在本次运行过程中编辑本页面的这些参数。\n本次校验通过的参数已经被保存, 下次打开时将会被重新加载，下次运行前，你仍可编辑这些参数。\n\n你刚才看到的警告是：\n%s\n\n你要继续吗？' % warning,
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            if r == QMessageBox.No:
                return

        run_classifier.setFlag(
            task_name='my_test',
            data_dir=file_parameters['data_dir'],
            bert_config_file=file_parameters['bert_config_file'],
            vocab_file=file_parameters['vocab_file'],
            output_dir=file_parameters['output_dir'],
            init_checkpoint=file_parameters['init_checkpoint'],

            do_lower_case=my_training_parameters[train_parameters.do_lower_case],
            max_seq_length=int(my_training_parameters[train_parameters.max_seq_length]),
            do_train=bool(my_training_parameters[train_parameters.do_train] == 'True'),
            do_eval=bool(my_training_parameters[train_parameters.do_eval] == 'True'),
            do_predict=bool(my_training_parameters[train_parameters.do_predict] == 'True'),
            train_batch_size=int(my_training_parameters[train_parameters.train_batch_size]),
            eval_batch_size=int(my_training_parameters[train_parameters.eval_batch_size]),
            predict_batch_size=int(my_training_parameters[train_parameters.predict_batch_size]),
            learning_rate=float(my_training_parameters[train_parameters.learning_rate]),
            num_train_epochs=float(my_training_parameters[train_parameters.num_train_epochs]),
            warmup_proportion=float(my_training_parameters[train_parameters.warmup_proportion]),
            save_checkpoints_steps=int(my_training_parameters[train_parameters.save_checkpoints_steps])
        )
        print('参数设置完毕')
        set_train_page_unable()
        print('此页面已禁用')
        run_test.bs.start()
        QMessageBox.warning(my_ui.my_page_train, '模型已经启动', '模型已经启动，请观察控制台输出消息。',
                            QMessageBox.Close)


def read_and_set_pie():
    print('先在开始分析')
    my_file_parameters = get_all_file_parameters()
    if os.path.isfile(os.path.join(my_file_parameters[file_parameters.output_dir], 'test_results.tsv')) is False:
        print('找不到文件')
        return


    # my_res=[a, b]
    cnt_80 = 0
    cnt_mid = 0
    cnt_20 = 0
    with open(os.path.join(my_file_parameters[file_parameters.output_dir], 'test_results.tsv'), 'r+', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        mynum = line.split('\t')
        if float(mynum[0]) < 0.2:
            cnt_20 += 1
        elif float(mynum[0]) < 0.8:
            cnt_mid += 1
        else:
            cnt_80 += 1

    draw_pie([cnt_20, cnt_mid, cnt_80], ['The Warning Message', 'Uncertainty Message', 'Safe Message'])


def draw_pie(num_list:list, my_label:list):
    global pie_ax
    global FC_train
    pie_ax.cla()
    pie_ax.set_title('The Predict Result of BERT Training')
    print('清除')
    pie_ax.pie(num_list, labels=my_label)
    FC_train.draw()
