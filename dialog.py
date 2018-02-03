# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt5.QtNetwork import QUdpSocket, QHostAddress


class UiDialog(QDialog):
    port_udp = 1345

    def __init__(self, dialog, parent=None):
        dialog.setObjectName("udp-test")
        dialog.resize(480, 400)

        super(UiDialog, self).__init__(parent)
        self.pushButton_2 = QtWidgets.QPushButton(dialog)
        self.pushButton = QtWidgets.QPushButton(dialog)
        self.textEdit = QtWidgets.QTextEdit(dialog)
        self.textEdit_port = QtWidgets.QTextEdit(dialog)
        self.textEdit_url = QtWidgets.QTextEdit(dialog)
        self.textBrowser = QtWidgets.QTextBrowser(dialog)
        self.udpSocket_sed = QUdpSocket()

        self.udpSocket_rev = QUdpSocket()
        # self.udpSocket_rev.bind(self.port_udp)
        self.udpSocket_rev.readyRead.connect(self.upd_rev)
        self.url = QHostAddress()
        self.url.setAddress("127.0.0.1")

        self.ret_ui(dialog)
        QtCore.QMetaObject.connectSlotsByName(dialog)

    def setup_ui(self):
        self.textBrowser.setGeometry(QtCore.QRect(40, 50, 301, 221))
        self.textBrowser.setObjectName("textBrowser")
        self.textEdit.setGeometry(QtCore.QRect(40, 290, 301, 74))
        self.textEdit.setObjectName("textEdit")
        self.textEdit_port.setGeometry(QtCore.QRect(360, 150, 113, 20))
        self.textEdit_port.setObjectName("textEdit_port")
        self.textEdit_url.setGeometry(QtCore.QRect(360, 200, 113, 20))
        self.textEdit_url.setObjectName("textEdit_url")
        self.pushButton.setGeometry(QtCore.QRect(360, 50, 113, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.upd_sed)
        self.pushButton_2.setGeometry(QtCore.QRect(360, 100, 113, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.port_ui)

    def ret_ui(self, dialog):
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle(_translate("udp-test", "udp网络测试工具"))
        self.pushButton.setText(_translate("udp-test", "发送"))
        self.pushButton_2.setText(_translate("udp-test", "确认端口及地址"))
        self.textEdit_port.setHtml(_translate("MainWindow",
                                              "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                              "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                              "p, li { white-space: pre-wrap; }\n"
                                              "</style></head><body style=\" font-family:\'.SF NS Text\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
                                              "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">1345</p></body></html>"))
        self.textEdit_url.setHtml(_translate("MainWindow",
                                             "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                             "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                             "p, li { white-space: pre-wrap; }\n"
                                             "</style></head><body style=\" font-family:\'.SF NS Text\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
                                             "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">127.0.0.1</p></body></html>"))

    def port_ui(self):
        self.port_udp = int(self.textEdit_port.toPlainText())
        self.url.setAddress(str(self.textEdit_url.toPlainText()))
        self.udpSocket_rev.bind(self.port_udp)

    def upd_rev(self):
        while self.udpSocket_rev.hasPendingDatagrams():
            datagram, host, port = self.udpSocket_rev.readDatagram(self.udpSocket_rev.pendingDatagramSize())

            try:
                # Python v3.
                datagram = str(datagram, encoding='utf-8')
            except TypeError:
                # Python v2.
                pass

            self.textBrowser.insertPlainText("发自 {}:{} 到 localhost:{}：\n".format(host.toIPv6Address()[-4:], port,
                                                                                 str(self.port_udp)) + datagram + '\n')

    def upd_sed(self):
        datagram = str(self.textEdit.toPlainText())
        self.udpSocket_sed.writeDatagram(datagram.encode("utf-8"), self.url, self.port_udp)


if __name__ == '__main__':
    '''
    主函数
    '''

    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    ui = UiDialog(mainWindow)
    ui.setup_ui()
    mainWindow.show()
    sys.exit(app.exec_())
