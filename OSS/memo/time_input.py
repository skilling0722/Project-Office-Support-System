# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTime
from PyQt5.QtCore import QPoint
import datetime
from popup import Popup



class Input_Time(QWidget):
    new_signal = QtCore.pyqtSignal()
    
    def __init__(self, parent=None):
        QWidget.__init__(self, parent = parent)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.center()
        self.resize(305,390)

        self.frame = QtWidgets.QWidget(self)
        self.frame.setEnabled(True)
        self.frame.setGeometry(QtCore.QRect(0,0,305,390))
        self.frame.setStyleSheet("background-color: #DACEFF; color: white; border-style: outset; border-radius: 10px; border-color: #AAAAAA; border-width: 2px")

        self.date_input = QtWidgets.QCalendarWidget(self)
        self.date_input.setGeometry(QtCore.QRect(10,20, 285, 270))
        self.date_input.setStyleSheet("QToolButton {color: rgb(0, 0, 0);};border-style: outset; border-radius: 5px; border-color: #AAAAAA; border-width: 1px")
        self.date_input.setGridVisible(True)
        self.date_input.setNavigationBarVisible(True)

        self.concat_time = ''

        self.time = QTime()
        self.current_time = self.time.currentTime()
        self.str_time = self.current_time.toString()

        self.time_input = QtWidgets.QTimeEdit(self.time, self)
        self.time_input.setGeometry(QtCore.QRect(110,300, 100, 30))
        self.time_input.setStyleSheet("background-color: #FFFFFF; color: black;border-style: outset; border-radius: 5px; border-color: white; border-width: 1px")

        set_time = datetime.datetime.now()  #현재시간 겟
        hh = int(str(set_time)[11:13])      #hh
        mm = int(str(set_time)[14:16])      #mm

        self.time_input.setTime(QTime(hh,mm))

        self.confirm_btn = QtWidgets.QPushButton(self)
        self.confirm_btn.setGeometry(QtCore.QRect(50, 340, 80, 40))
        self.confirm_btn.setStyleSheet("background-color: #BB00F4; color: white; border-style: outset; border-radius: 10px; border-color: #AAAAAA; border-width: 1px")

        self.cancle_btn = QtWidgets.QPushButton(self)
        self.cancle_btn.setGeometry(QtCore.QRect(170, 340, 80, 40))
        self.cancle_btn.setStyleSheet("background-color: #BB00F4; color: white; border-style: outset; border-radius: 10px; border-color: #AAAAAA; border-width: 1px")

        self.confirm_btn.clicked.connect(lambda: self.confirm())
        self.cancle_btn.clicked.connect(lambda: self.cancle())

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.confirm_btn.setText(_translate("Form", "확인"))
        self.cancle_btn.setText(_translate("Form", "취소"))

    def confirm(self):
        date = self.get_date()
        time = self.get_time()
        
        #self.popup = Popup(self)
        #self.popup.setGeometry(0,0,100,100)
        #self.popup.input_time_success()
        #self.popup.show()
        #self.popup.new_signal.connect(self.complete)

        self.concat_time = date + ' ' + time
        self.complete()

    def get_date(self):
        date = self.date_input.selectedDate().toString("yyyy-MM-dd")
        return date

    def get_time(self):
        time = self.time_input.time().toString("hh:mm:ss")
        return time

    def complete(self):
        self.new_signal.emit()
        self.deleteLater()

    def cancle(self):
        self.deleteLater()
        
    def center(self):
        move = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        move.moveCenter(cp)
        self.move(move.topLeft())

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Memo_widget()
    #Form.show()
    sys.exit(app.exec_())

