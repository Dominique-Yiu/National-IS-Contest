import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import QtWidgets
from untitled import Ui_MainWindow
from adc_collect import collect_data
from envelope_process import envelope
import numpy as np
from variance import window_var
from patternmatch import pattern_match
import threading
from modify_features import *


def eliminate(data=None):
    return data





class operate(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(operate, self).__init__()
        self.setupUi(self)
        self.collector = collect_data(port='COM5', m_time=1)

    def processing_data(self):
        name = self.lineEdit_2.text()
        gross_data = []
        for i in range(8):
            filtered_data = self.collector.start(load_path=None, save_path=None, m_time=10)
            # remove the unstable data (the first 0.5 seconds)
            filtered_data = filtered_data[int(2302 * 0.5):]
            rhythm_number = self.collector.get_rhythm_number()
            upper, _ = envelope(filtered_data, 100).start()
            # 这里包含放手和松手的时间点，后面需要去重
            end_points, _ = window_var(data=upper, head=rhythm_number).start()
            start_points = pattern_match(data=upper, number=rhythm_number).start()
            start_points = np.array(start_points)
            features = np.append(end_points, start_points)
            '''
            缺少一个去重函数具体实现
            '''
            features = eliminate(features)
            gross_data.append(features)
        gross_data = np.array(gross_data)
        add_modify(add_data=gross_data, add_name=name)

    def start_measure(self):
        threading.Thread(target=self.processing_data)
        self.recv_thread.start()
        #     self.textBrowser_2.setText(f"已收集第{i}次数据")
        # QMessageBox.information(self, '提示信息', '按钮1被按下。')

    def start_certificate(self):
        QMessageBox.information(self, '提示信息', '按钮1被按下。')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    my_pyqt_form = operate()
    my_pyqt_form.show()
    sys.exit(app.exec_())
