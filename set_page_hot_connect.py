import MainWindow
import wordcloud
# matplotlib 和qt链接的包
# 修复打包的问题
import matplotlib
matplotlib.use("Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from c_word_cloude import word_clouad_create


def set_page_connect(ui: MainWindow.Ui_MainWindow):
    global ax_wc_r
    global ax_wc_l
    global my_ui
    global FC_hot  # 画图组件
    my_ui = ui

    # 命令按钮
    my_ui.my_page_hot_commandLinkButton_menu_run.clicked.connect(go_for_run_word_cloud)

    word_clouad_create.word_cloude_create.send_graph_process_bar.connect(set_hot_process_bar)

    # 初始化画板
    f = plt.figure()
    FC_hot = FigureCanvas(f)

    # 小图
    ax_wc_l = f.add_subplot(1,2,1)
    ax_wc_r = f.add_subplot(1,2,2)
    # 大画板!!!!!!!!!!!!!!!!!!!!!!
    my_ui.my_page_hot_gridLayout_for_graph.layout().addWidget(FC_hot)
    word_clouad_create.word_cloude_create.send_cloude_dict.connect(set_cloud)

    set_cloud({"等待分析": 1.0}, {"等待分析": 1.0})


def go_for_run_word_cloud():
    word_clouad_create.word_cloude_create.set_path(my_ui.my_page_corpus_lineEdit_workPath.text())
    word_clouad_create.word_cloude_create.start()


def set_cloud(a: dict, b: dict):
    global ax_wc_r
    global ax_wc_l
    global FC_hot

    wc1 = wordcloud.WordCloud(font_path='STXINGKA.TTF', height=460, width=500, background_color='white')
    wc2 = wordcloud.WordCloud(font_path='STXINGKA.TTF', height=460, width=500, background_color='white')
    wc1.generate_from_frequencies(a)
    wc2.generate_from_frequencies(b)
    ax_wc_l.set_title("Heat clouds of Message")
    ax_wc_l.imshow(wc1)
    ax_wc_l.axis('off')

    ax_wc_r.set_title("Dispels the top 20 for subsidiary")
    ax_wc_r.imshow(wc2)
    ax_wc_r.axis('off')
    FC_hot.draw()


def set_hot_process_bar(setp_process: int):
    global my_ui
    my_ui.my_page_hot_progressBar.setValue(setp_process)
