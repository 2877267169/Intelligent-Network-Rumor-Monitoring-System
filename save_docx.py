import os

from PyQt5.QtWidgets import QMessageBox, QFileDialog
import docx

import MainWindow
from main_window_run import my_app_img_dir

def save_docx(ui: MainWindow.Ui_MainWindow):
    """
    将缓存中的图片导出为报告
    :param ui:  界面
    :return: None
    """
    base_dir = my_app_img_dir
    if (
        os.path.isfile(os.path.join(base_dir, "corpus.png")) and
        os.path.isfile(os.path.join(base_dir, "train_res.png")) and
        os.path.isfile(os.path.join(base_dir, "ana_A.png")) and
        os.path.isfile(os.path.join(base_dir, "ana_B.png")) and
        os.path.isfile(os.path.join(base_dir, "ana_C.png")) and
        os.path.isfile(os.path.join(base_dir, "ana_D.png")) and
        os.path.isfile(os.path.join(base_dir, "warning.png")) and
        os.path.isfile(os.path.join(base_dir, "word_cloud.png"))
    ) is True:
        filename_choose, _ = QFileDialog.getSaveFileName(
            ui.statusbar,
            "Export Docx Report...",
            '.',  # 起始路径
            "Office Document Files (*.docx)"
        )
        print("从缓存加载..")
        # ######################## 开始了docx的处理 #################
        doc = docx.Document(r"Template/Template.docx")
        for i, p in enumerate(doc.paragraphs):
            if '.图1.' in p.text:
                p.runs[0].add_break()  # 添加一个折行
                p.runs[0].add_picture(os.path.join(base_dir, "corpus.png"))  # 在runs的最后一段文字后添加图片
            if '.图2.' in p.text:
                p.runs[0].add_break()  # 添加一个折行
                p.runs[0].add_picture(os.path.join(base_dir, "train_res.png"))
            if '.图3.' in p.text:
                p.runs[0].add_break()  # 添加一个折行
                p.runs[0].add_picture(os.path.join(base_dir, "ana_A.png"))
            if '.图4.' in p.text:
                p.runs[0].add_break()  # 添加一个折行
                p.runs[0].add_picture(os.path.join(base_dir, "ana_C.png"))
            if '.图5.' in p.text:
                p.runs[0].add_break()  # 添加一个折行
                p.runs[0].add_picture(os.path.join(base_dir, "ana_B.png"))
            if '.图6.' in p.text:
                p.runs[0].add_break()  # 添加一个折行
                p.runs[0].add_picture(os.path.join(base_dir, "ana_D.png"))
            if '.图7.' in p.text:
                p.runs[0].add_break()  # 添加一个折行
                p.runs[0].add_picture(os.path.join(base_dir, "warning.png"))
            if '.图8.' in p.text:
                p.runs[0].add_break()  # 添加一个折行
                p.runs[0].add_picture(os.path.join(base_dir, "word_cloud.png"))
        doc.save(filename_choose)
    else:
        QMessageBox.critical(ui.statusbar, "Error", "文件不完整。")
        print("文件不完整")

