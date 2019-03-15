# -*- coding: utf-8 -*-
import sys, os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QObject
from general_memo import General_Memo
from alarm_memo import Alarm_Memo
from view_memo import View_Memo
from view_alarm_memo import View_Alarm_Memo
from time_input import Input_Time
import memo_db
from User_info import User_Notice
from pygame import mixer


#dup_check = 0
alarm_list = []


class Ui_Memo_widget(QWidget, User_Notice):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent = parent)

        self.resize(650, 520)
        self.setMinimumSize(QtCore.QSize(650, 520))
        self.setMaximumSize(QtCore.QSize(650, 520))

        self.display_frame = QtWidgets.QFrame(self)
        self.display_frame.setGeometry(QtCore.QRect(30, 10, 530, 440))
        self.display_frame.setStyleSheet("background-color: white;border-style: outset; border-width: 0px")

        self.gridLayout = QtWidgets.QGridLayout(self.display_frame)
        self.scrollArea = QtWidgets.QScrollArea(self.display_frame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(30, 10, 530, 440))
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)

        self.db_time = ''
        self.user_name = User_Notice.get_id()
        self.memo_count = memo_db.count_memo(self.user_name)
        self.get_memo()
        

        frame_lists = self.create_var_memo(self.memo_count, self.memo_collect)

        for frame in frame_lists:
            self.display(frame)


        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 1, 1, 1)

        self.create_Gmemo = QtWidgets.QPushButton(self)
        self.create_Gmemo.setGeometry(QtCore.QRect(185, 460, 80, 40))
        self.create_Gmemo.setStyleSheet("background-color: #414141; color: white;border-style: outset; border-radius: 5px; border-color: black; border-width: 1px")

        self.create_Amemo = QtWidgets.QPushButton(self)
        self.create_Amemo.setGeometry(QtCore.QRect(330, 460, 80, 40))
        self.create_Amemo.setStyleSheet("background-color: #414141; color: white;border-style: outset; border-radius: 5px; border-color: black; border-width: 1px")

        self.delete_memo = QtWidgets.QPushButton(self)
        self.delete_memo.setGeometry(QtCore.QRect(475, 460, 80, 40))
        self.delete_memo.setStyleSheet("background-color: #414141; color: white;border-style: outset; border-radius: 5px; border-color: black; border-width: 1px")



        self.create_Gmemo.clicked.connect(lambda: self.create_Gmemo_method())
        self.create_Amemo.clicked.connect(lambda: self.create_Amemo_method())
        self.delete_memo.clicked.connect(lambda: self.remove_memo())

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

        
        self.alarm = Alarm()
        self.alarm.update_signal.connect(self.display_update)
        self.alarm.view_signal.connect(self.alarm_view)
        

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        
        self.create_Gmemo.setText(_translate("Form", "메모 생성"))
        self.create_Amemo.setText(_translate("Form", "알람메모 생성"))
        self.delete_memo.setText(_translate("Form", "삭제"))

    def create_Gmemo_method(self):
        #if dup_check == 1:
        #    dialog = QMessageBox()
        #    dialog.setWindowTitle("에러")
        #    dialog.setText("기존 작업을 취소한 후 시도해주세요.")
        #    dialog.setIcon(QMessageBox.Warning)
        #    dialog.exec_()
        #else:
        self.GMemo = General_Memo(self)
        self.GMemo.show()

        self.GMemo.new_signal.connect(self.display_update)
            #dup_check = 1

    def create_Amemo_method(self):
        #if dup_check == 1:
        #    dialog = QMessageBox()
        #    dialog.setWindowTitle("에러")
        #    dialog.setText("기존 작업을 취소한 후 시도해주세요.")
        #    dialog.setIcon(QMessageBox.Warning)
        #    dialog.exec_()
        #else:
        self.AMemo = Alarm_Memo(self)
        self.AMemo.show()
            
        self.AMemo.new_signal.connect(self.display_update)
        #dup_check = 1

    def display(self, frame_list):
        
        #print("framelist: ", frame_list)
        #메모 ID [6][0]
        #메모 타입 frame_list[6][1]
        #메모 시간 frame_list[6][4]
        #메모 제목 [6][2]
        #메모 내용 [6][3]
        
        if frame_list[6][1] == 1:
            time = str(frame_list[6][4])

            alarm_date = time[0:10]
            alarm_time = time[11:16]

            alarm_list.append(alarm_date + " " + alarm_time)
            #self.alarm_lists.append(alarm_date + " " + alarm_time)
            print(alarm_list)

        frame_list[1] = QGroupBox('', self.scrollAreaWidgetContents)
        frame_list[1].setStyleSheet("background-color: white; color: #BBBBBB;border-style: solid; border-radius: 5px; border-color: #DDDDDD; border-width: 0px")

        frame_list[2] = QtWidgets.QHBoxLayout(frame_list[1])

        frame_list[3] = QtWidgets.QRadioButton(frame_list[1])           #체크
        frame_list[3].setMaximumSize(QtCore.QSize(30,30))
        frame_list[3].setStyleSheet("border-style: solid; border-width: 0px")

        frame_list[4] = QtWidgets.QPushButton(frame_list[1])            #메모 제목. 클릭하면 view
        if frame_list[6][1] == 0:
            frame_list[4].setStyleSheet("background-color: #EAFFDB; color: black;border-style: outset; border-radius: 5px; border-color: #8BF74C; border-width: 2px")
        else:
            frame_list[4].setStyleSheet("background-color: #DACEFF; color: black;border-style: outset; border-radius: 5px; border-color: #8860FF; border-width: 2px")
        frame_list[4].setMinimumSize(QtCore.QSize(100,30))

        frame_list[4].setText(frame_list[6][2]) #디비 메모 제목

        title_font = frame_list[4].font()
        title_font.setPointSize(12)
        title_font.setBold(True)
        frame_list[4].setFont(title_font)

        frame_list[5] = QtWidgets.QPushButton(frame_list[1])            #알람 <-> 일반 전환
        frame_list[5].setText("전환")
        frame_list[5].setMaximumSize(QtCore.QSize(30,30))
        if frame_list[6][1] == 0:
            frame_list[5].setStyleSheet("background-color: #EAFFDB; color: black;border-style: outset; border-radius: 5px; border-color: #8BF74C; border-width: 2px")       
        else:
            frame_list[5].setStyleSheet("background-color: #DACEFF; color: black;border-style: outset; border-radius: 5px; border-color: #8860FF; border-width: 2px")   

        frame_list[2].addWidget(frame_list[3])
        frame_list[2].addWidget(frame_list[4])
        frame_list[2].addWidget(frame_list[5])
        
        if frame_list[6][1] == 0:
            frame_list[4].clicked.connect(lambda: self.view_memo(frame_list[6][3], frame_list[6][2]))
            frame_list[5].clicked.connect(lambda: self.general_to_alarm(frame_list[6][0], frame_list[6][2]))
            #self.view_memo(frame_list[6][3], frame_list[6][2])
        else:
            frame_list[4].clicked.connect(lambda: self.view_alarm_memo(frame_list[6][3], frame_list[6][2], frame_list[6][4]))
            frame_list[5].clicked.connect(lambda: self.alarm_to_general(frame_list[6][0], frame_list[6][2]))
            #self.view_alarm_memo(frame_list[6][3], frame_list[6][2], frame_list[6][4])
        
        
        
        
        self.verticalLayout.addWidget(frame_list[1])

    def alarm_to_general(self, user_name, title):
        
        memo_db.alarm_to_general(user_name, title)

        self.display_update()

    def general_to_alarm(self, user_name, title):
        self.input_time = Input_Time()
        self.input_time.show()

        self.input_time.new_signal.connect(lambda: self.general_to_alarm_db(user_name, title))

        

    def general_to_alarm_db(self, user_name, title):
        memo_db.general_to_alarm(self.input_time.concat_time, user_name, title)

        self.display_update()

    def view_memo(self, content, title):
        self.content = View_Memo(self)
        self.content.show()

        self.content.memo_content(content)
        self.content.memo_title(title)

        #self.content.general_signal.connect(lambda: self.memo_close(self.view_list[0]))


    def view_alarm_memo(self, content, title, time):
        self.content = View_Alarm_Memo(self)
        self.content.show()

        self.content.memo_content(content)
        self.content.memo_title(title)
        self.content.memo_time(time)

    def alarm_view(self):
        self.cur_date = QtCore.QDate.currentDate()
        self.cur_time = QtCore.QTime.currentTime()
        
        str_date = self.cur_date.toString('yyyy-MM-dd')
        str_time = self.cur_time.toString('hh:mm')
        
        date_time = str_date + ' ' + str_time
        
        result = memo_db.alarm_view(self.user_name, date_time)[0]

        self.view_alarm_memo(result[1], result[0], result[2])


    def display_update(self):
        self.memo_count = memo_db.count_memo(self.user_name)
        self.get_memo()

        for i in reversed(range(self.verticalLayout.count())):
            self.verticalLayout.itemAt(i).widget().setParent(None)

        global alarm_list
        alarm_list = []

        frame_lists = self.create_var_memo(self.memo_count, self.memo_collect)

        for frame in frame_lists:
            self.display(frame)

        self.display_frame.update()
    
    def find_child(self):
        child_list_radio = self.findChildren(QtWidgets.QRadioButton)
        child_list_groupbox = self.findChildren(QtWidgets.QGroupBox)
        return child_list_radio, child_list_groupbox

    def remove_memo(self):
        self.get_memo()
        list_radio, list_groupbox = self.find_child()

        for i in range(0, self.memo_count):
            if list_radio[i].isChecked():
                for g in range(0, self.memo_count):
                    child = list_groupbox[g].findChildren(QtWidgets.QRadioButton)
                    if list_radio[i] == child[0]:
                        ##########################################################################################
                        child_button = list_groupbox[g].findChildren(QtWidgets.QPushButton)
                        
                        title = child_button[0].text()      #삭제할 메모 제목 겟

                        ###########################################################################################
                        db_memo_time = str(memo_db.get_time(self.user_name, title)[0])  #삭제할 시간 겟 알람리스트에 있는 시간 없애야댐
                        if db_memo_time != '0000-00-00 00:00:00':   #알람메모 처리
                            db_alarm_date = db_memo_time[0:10]              #날짜 추출
                            db_alarm_time = db_memo_time[11:16]             #시간 추출
                            
                            self.db_time = db_alarm_date + " " + db_alarm_time  #합쳐

                            try:
                                alarm_list.remove(self.db_time)     #재생을 위한 리스트에서 삭제해줘
                                #알람 삭제
                            except:
                                #리스트에 없음
                                pass
                        else:
                            pass            #일반메모라서 처리 안해줌
                        ###########################################################################################


                        memo_db.delete_memo(self.user_name, title)          #DB에서도 메모 삭제

                        list_groupbox[g].deleteLater()      #GUI 에서 메모 삭제
                        self.memo_count = memo_db.count_memo(self.user_name)
                        
    

    def create_var_memo(self, memo_count, DB_memo):
        frame_lists = []
        
        for i in range(0, memo_count):
            frame_list = []
            memo_var = ""
            zero_var = "zero_var"+str(i)
            first_var = "first_var"+str(i)
            second_var = "second_var"+str(i)
            third_var = "third_var"+str(i)
            fourth_var = "fourth_var"+str(i)

            frame_list.append(memo_var)
            frame_list.append(zero_var)
            frame_list.append(first_var)
            frame_list.append(second_var)
            frame_list.append(third_var)
            frame_list.append(fourth_var)
            frame_list.append(DB_memo[i])

            frame_lists.append(frame_list)

        return frame_lists

    def get_memo(self):
        self.memo_collect = memo_db.view_memo(self.user_name)



class Alarm(QObject, User_Notice):

    update_signal = QtCore.pyqtSignal()
    view_signal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.timer = QtCore.QTimer()
        self.timer.start(1000)
        self.timer.timeout.connect(self.timeout)
        self.user_name = User_Notice.get_id()

    def timeout(self):
        self.cur_date = QtCore.QDate.currentDate()
        self.cur_time = QtCore.QTime.currentTime()
        
        str_date = self.cur_date.toString('yyyy-MM-dd')
        str_time = self.cur_time.toString('hh:mm')
        
        date_time = str_date + ' ' + str_time

        for alarm in alarm_list:
            if alarm == date_time:

                memo_db.change_memo(self.user_name, alarm)

                self.sound()

                self.update_signal.emit()
                self.view_signal.emit()
                
    def sound(self):
        mixer.init()
        song = mixer.music.load(os.getcwd()+'/sound/alarm.wav')
        mixer.music.play()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Memo_widget()
    #Form.show()
    sys.exit(app.exec_())

