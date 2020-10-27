import os

from PyQt5.QtWidgets import QMessageBox, QFileDialog
import docx
from docx.shared import Cm
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
                p.runs[0].add_picture(os.path.join(base_dir, "corpus.png"), width=Cm(14.64))  # 在runs的最后一段文字后添加图片
                p.runs[0].add_break()  # 添加一个折行
            if '.图2.' in p.text:
                p.runs[0].add_break()  # 添加一个折行
                p.runs[0].add_picture(os.path.join(base_dir, "train_res.png"), width=Cm(14.64))
                p.runs[0].add_break()  # 添加一个折行
            if '.图3.' in p.text:
                p.runs[0].add_break()  # 添加一个折行
                p.runs[0].add_picture(os.path.join(base_dir, "ana_A.png"), width=Cm(14.64))
                p.runs[0].add_break()  # 添加一个折行
            if '.图4.' in p.text:
                p.runs[0].add_break()  # 添加一个折行
                p.runs[0].add_picture(os.path.join(base_dir, "ana_C.png"), width=Cm(14.64))
                p.runs[0].add_break()  # 添加一个折行
            if '.图5.' in p.text:
                p.runs[0].add_break()  # 添加一个折行
                p.runs[0].add_picture(os.path.join(base_dir, "ana_B.png"), width=Cm(8))
                p.runs[0].add_break()  # 添加一个折行
            if '.图6.' in p.text:
                p.runs[0].add_break()  # 添加一个折行
                p.runs[0].add_picture(os.path.join(base_dir, "ana_D.png"), width=Cm(8))
                p.runs[0].add_break()  # 添加一个折行
            if '.图7.' in p.text:
                p.runs[0].add_break()  # 添加一个折行
                p.runs[0].add_picture(os.path.join(base_dir, "warning.png"), width=Cm(14.64))
                p.runs[0].add_break()  # 添加一个折行
            if '.图8.' in p.text:
                p.runs[0].add_break()  # 添加一个折行
                p.runs[0].add_picture(os.path.join(base_dir, "word_cloud.png"), width=Cm(14.64))
                p.runs[0].add_break()  # 添加一个折行
        try:
            doc.save(filename_choose)
            QMessageBox.information(ui.statusbar, "完成", "成功完成了生成", QMessageBox.Ok)

        except:
            QMessageBox.critical(
                ui.statusbar, "Error", "发生了一些错误\n请检查是否有足够的权限访问，或目标文件处于是否处于占用状态。"
            )
    else:
        QMessageBox.critical(ui.statusbar, "Error", "文件不完整。")
        print("文件不完整")
