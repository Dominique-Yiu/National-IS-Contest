# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
import random


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(423, 672)
        MainWindow.setMinimumSize(QtCore.QSize(331, 0))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_3 = QtWidgets.QLabel(self.tab)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 2)
        self.textBrowser = QtWidgets.QTextBrowser(self.tab)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout_2.addWidget(self.textBrowser, 1, 2, 1, 6)
        self.label_4 = QtWidgets.QLabel(self.tab)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 2, 0, 1, 3)
        self.comboBox_3 = QtWidgets.QComboBox(self.tab)
        self.comboBox_3.setObjectName("comboBox_3")
        self.gridLayout_2.addWidget(self.comboBox_3, 3, 1, 1, 4)
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 2)
        self.progressBar = QtWidgets.QProgressBar(self.tab)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout_2.addWidget(self.progressBar, 5, 0, 1, 4)
        self.pushButton_4 = QtWidgets.QPushButton(self.tab)
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout_2.addWidget(self.pushButton_4, 4, 6, 1, 2)
        self.label_6 = QtWidgets.QLabel(self.tab)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 3, 5, 1, 2)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout_2.addWidget(self.lineEdit_2, 3, 7, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.tab)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_2.addWidget(self.lineEdit, 0, 2, 1, 6)
        self.comboBox_2 = QtWidgets.QComboBox(self.tab)
        self.comboBox_2.setObjectName("comboBox_2")
        self.gridLayout_2.addWidget(self.comboBox_2, 2, 3, 1, 5)
        self.label_5 = QtWidgets.QLabel(self.tab)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 3, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.tab)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_2.addWidget(self.pushButton, 4, 0, 1, 4)
        self.pushButton_3 = QtWidgets.QPushButton(self.tab)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout_2.addWidget(self.pushButton_3, 4, 4, 1, 2)
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.tab)
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.gridLayout_2.addWidget(self.textBrowser_2, 5, 4, 1, 4)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.pushButton_2 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 10, 301, 21))
        self.pushButton_2.setObjectName("pushButton_2")
        self.textBrowser_4 = QtWidgets.QTextBrowser(self.tab_2)
        self.textBrowser_4.setGeometry(QtCore.QRect(10, 60, 301, 191))
        self.textBrowser_4.setObjectName("textBrowser_4")
        self.tabWidget.addTab(self.tab_2, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 2)
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 397, 150))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.textBrowser_3 = QtWidgets.QTextBrowser(self.scrollAreaWidgetContents)
        self.textBrowser_3.setObjectName("textBrowser_3")
        self.gridLayout_3.addWidget(self.textBrowser_3, 1, 0, 1, 5)
        self.label_7 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_7.setObjectName("label_7")
        self.gridLayout_3.addWidget(self.label_7, 0, 0, 1, 1)
        self.comboBox_4 = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.comboBox_4.setObjectName("comboBox_4")
        self.gridLayout_3.addWidget(self.comboBox_4, 0, 1, 1, 1)
        self.pushButton_5 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayout_3.addWidget(self.pushButton_5, 0, 2, 1, 1)
        self.pushButton_6 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_6.setObjectName("pushButton_6")
        self.gridLayout_3.addWidget(self.pushButton_6, 0, 3, 1, 1)
        self.pushButton_7 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_7.setObjectName("pushButton_7")
        self.gridLayout_3.addWidget(self.pushButton_7, 0, 4, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 423, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.pushButton.clicked.connect(MainWindow.start_measure)
        self.pushButton_2.clicked.connect(MainWindow.start_certificate)
        self.lineEdit.returnPressed.connect(MainWindow.manage_certificate)
        self.pushButton_3.clicked.connect(MainWindow.delete_user)
        self.pushButton_4.clicked.connect(MainWindow.modify_rhythm)
        self.pushButton_5.clicked.connect(MainWindow.open_port)
        self.pushButton_6.clicked.connect(MainWindow.get_intensity)
        self.pushButton_7.clicked.connect(MainWindow.plot_series)
        self.comboBox_4.currentTextChanged['QString'].connect(MainWindow.port_changed)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.tabWidget.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>是</p></body></html>"))
        self.label_3.setText(_translate("MainWindow", "当前信息"))
        self.label_4.setText(_translate("MainWindow", "选择要进行的操作"))
        self.label.setText(_translate("MainWindow", "验证PIN码"))
        self.pushButton_4.setText(_translate("MainWindow", "重置节奏"))
        self.label_6.setText(_translate("MainWindow", "输入新用户姓名"))
        self.label_5.setText(_translate("MainWindow", "指定用户"))
        self.pushButton.setText(_translate("MainWindow", "开始录入节奏信息"))
        self.pushButton_3.setText(_translate("MainWindow", "确认删除"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "管理员登录"))
        self.pushButton_2.setText(_translate("MainWindow", "开始进行验证"))
        self.textBrowser_4.setHtml(_translate("MainWindow",
                                              "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                              "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                              "p, li { white-space: pre-wrap; }\n"
                                              "</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                              "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "老用户认证"))
        self.label_7.setText(_translate("MainWindow", "串口选择"))
        self.pushButton_5.setText(_translate("MainWindow", "打开串口"))
        self.pushButton_6.setText(_translate("MainWindow", "检测环境噪声"))
        self.pushButton_7.setText(_translate("MainWindow", "串口绘图器"))


import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import os
import sys

matplotlib.use('Qt5Agg')


class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        raise NotImplementedError


import numpy as np


class MyDynamicMplCanvas(MyMplCanvas):
    """A canvas that updates itself every second with a new plot."""

    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(50)

    def compute_initial_figure(self):
        show_data = get_value()
        self.axes.plot(show_data)

    def update_figure(self):
        show_data = get_value()
        self.axes.cla()
        self.axes.plot(show_data)
        self.draw()


class plot_window(QWidget):
    def __init__(self, parent=None):
        super(plot_window, self).__init__(parent)
        self.setWindowTitle("排列组合")
        self.resize(700, 400)
        widget = QWidget()
        layout = QGridLayout()
        picture = MyDynamicMplCanvas(widget, width=5, height=4, dpi=100)
        layout.addWidget(picture, 0, 0, 1, 1)

        self.setLayout(layout)

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, '警告', '退出后测试将停止,你确认要退出吗？', QtWidgets.QMessageBox.Yes,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            plot_collector.ser.close()
            event.accept()
        else:
            event.ignore()


from adc_collect import collect_data

plot_collector = collect_data(port='COM3')

plot_data = np.zeros(100)
def get_value():
    # show_data = np.zeros(100)
    plot_data[:95] = plot_data[5:]
    for i in range(5):
        try:
            plot_data[i + 95] = plot_collector.ser.readline()
        except:
            pass
    return plot_data

# if __name__ == "__main__":
#         app = QApplication(sys.argv)
#         form = plot_window()
#         form.show()
#         sys.exit(app.exec_())
