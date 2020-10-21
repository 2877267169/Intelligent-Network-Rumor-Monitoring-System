import time
from analysis import analysis_processer


def show_time(start_t, p):
    analysis_processer.analise_message.f_send_my_analyse_process_bar(int(p * 100))  # 调整进度条
    if p == 0:
        return
    now_t = time.time()
    t = now_t - start_t
    ana = (t / p) * (1 - p)
    message = "已用时 %.2f 秒(%.1f 分钟)" % (t, t / 60)
    message2 = message + "\n预计剩余 %.2f 秒(%.1f 分钟)\n预计完成时间 %s." % (
        ana, ana / 60, time.asctime(time.localtime(now_t + ana))
    )
    message += "预计剩余 %.2f 秒(%.1f 分钟), 预计完成时间 %s." % (ana, ana / 60, time.asctime(time.localtime(now_t + ana)))

    print(message)
    analysis_processer.analise_message.f_send_text_message(message2)
