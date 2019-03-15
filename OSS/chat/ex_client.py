from threading import Thread
import socket
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *


from User_info import User_Notice    #a
import time #a
import json
'''
로그인화면 => 메인화면: 아이디/닉네임/이메일은 저장해두어야함. 설정, 채팅, 파일관리, 메모때문에 필요함.
'''

class Chat_Client(QtCore.QThread, QtCore.QObject, User_Notice):
    new_signal = QtCore.pyqtSignal()            ##event신호 할당

    def __init__(self,host,port, name): ##name은 db에서 가져온거 넣어라, threadid
        super().__init__()
        self.host = host
        self.port = port
        self.name = name
        self.running = False #a
        self.sock = None     #a
    def set_sock(self):
        try:
            self.sock= socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        except socket.error as exc:                         
            print('server connect error', exc)

        try:
            self.sock.connect((self.host, self.port))
        except socket.error as exc:                         ##server->socket server connect-> error
            print('chatting connect error:', exc)
        except socket.timeout as time:                      ##server connect-> error
            print('[time_error]', time)
        else:
            print('chatting server connect')

    
    def set_name(self, name):
        if name != None:
            self.name = name
        else:
            self.name = "error_name"
   
    def msg_to_client(self, _msg):
        try:
            self.sock.send(_msg.encode('utf-8'))
        except socket.error as exc:
            print('msg_to_client():, 채팅연결실패', exc)
            pass

    def wel_msg(self):  #0
        msg = {'flag':'0', 'name':self.name, 'content':'님이 들어왔어요'}
        msg = json.dumps(msg)
        self.msg_to_client(msg)

    def bye_msg(self):  #1
        msg = {'flag':'1', 'name':self.name, 'content':'님이 나갔어요'}
        msg = json.dumps(msg)
        self.msg_to_client(msg)
        
    def get_msg(self, msg): #2
        if len(msg) == 0:     
            pass
        else:
            self.name = User_Notice.get_id()
            send_msg = {'flag':'2', 'name':self.name, 'content':msg}
            send_msg = json.dumps(send_msg)
            self.msg_to_client(send_msg)             

    def file_msg(self):   #3
        msg = {'flag':'3', 'name':self.name, 'content':'님이 파일보냈어요.'}
        msg = json.dumps(msg)
        self.msg_to_client(msg)

   ##################################################################################################################
#
    ###a
    def run(self):
        self.set_sock()
        print("-chatting Thread Run-")       ##[screen]채팅에 오신걸 환영합니다.
        self.wel_msg()
        time.sleep(1)
        ##메시지받기 인스턴스생성## 쓰레드돌리기 #slepp(1)
        self.running = True
        while self.running:
            try:
                self.data = self.sock.recv(1024)
                self.data = self.data.decode("utf-8")
                if self.running:
                    self.new_signal.emit()
                else:
                    break
            except socket.error as e:
                print('[Errno-thread]', e)
                break
            except Exception as e:
                print('[Errno-thread]', e)
                break
        try:
            self.sock.close()     #있어야 포트랑 프로세스 닫히지 않나?
        except:
            pass
        print('thread exit')
   
   ###a 
    def stop(self):
        self.running = False

    def msg_token(self):
        try:
            json_msg = json.loads(self.data)
        except:
            json_msg = None
            print('json_msg: None')
        finally:
            return json_msg
