from bert import run_classifier
import tensorflow as tf
# exec('run_classifier')


from PyQt5.QtCore import QThread, pyqtSignal


class BertRun(QThread):
    def run(self):
        try:
            run_classifier.my_run()
        except:
            print('finished,  ut you must chk something.')


bs = BertRun()

"""run_classifier.setFlag(
        task_name="my_test",
        do_train=True,
        data_dir=r"./data/顶替_大学",
        vocab_file=r'./dict/chinese_L-12_H-768_A-12/vocab.txt',
        bert_config_file=r'./dict/chinese_L-12_H-768_A-12/bert_config.json',
        init_checkpoint=r'./dict/chinese_L-12_H-768_A-12/bert_model.ckpt',
        max_seq_length=128,
        train_batch_size=32,
        learning_rate=2e-5,
        num_train_epochs=3.0,
        output_dir=r'./out_put/顶替_大学_output/'
    )
if __name__ == '__main__':
    tf.app.run(run_classifier.go)
print('fifished')"""
