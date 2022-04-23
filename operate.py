import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import QtWidgets
from untitled import Ui_MainWindow
from adc_collect import collect_data
from envelope_process import envelope
import numpy as np
from variance import window_var
from patternmatch import pattern_match


class operate(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(operate, self).__init__()
        self.setupUi(self)
        self.collector = collect_data(port='COM5', m_time=1)

    def start_measure(self):
        name = self.lineEdit_2.text()
        name_list = np.loadtxt('name.csv')
        name_list = np.append(name_list, name)
        np.savetxt('name.csv', name_list)
        for i in range(2):
            L_path = name + '_' + str(i) + '.csv'
            S_path = name + '_' + 'filtered_' + str(i) + '.csv'
            self.collector.start(load_path=L_path, save_path=S_path, m_time=1)
            upper, _ = envelope(self.collector.filter.filtered_data, 100).start()
            # np.savetxt(name + '_envelope_data' + '_' + str(i) + '.csv', upper)
            end_points, _ = window_var(data=upper).start()
            start_points = pattern_match(data=upper).start()
            start_points = np.array(start_points)
            features = np.append(end_points, start_points)
            self.textBrowser_2.setText(f"已收集第{i}次数据")
        QMessageBox.information(self, '提示信息', '按钮1被按下。')

    def start_certificate(self):
        QMessageBox.information(self, '提示信息', '按钮1被按下。')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    my_pyqt_form = operate()
    my_pyqt_form.show()
    sys.exit(app.exec_())
