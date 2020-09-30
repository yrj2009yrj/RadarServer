from PyQt5.QtCore import pyqtSignal, QObject, QTimer
from PyQt5.QtWebSockets import QWebSocket

from protoc.SendData_pb2 import SendData

from Utils import *


class ReplyTrack(QObject):
    def __init__(self, parent=None):
        super(ReplyTrack, self).__init__(parent)

        self.timer = {}
        self.reply = {}

    def add_track(self, data: SendData):
        serial = data.seriaNum
        timer_id = self.startTimer(5000)
        self.timer[serial] = timer_id
        self.reply[timer_id] = data

    def remove_track(self, serial):
        timer_id = self.timer[serial]
        self.killTimer(timer_id)
        del self.timer[serial]
        del self.reply[timer_id]

    def timerEvent(self, event):
        data = self.reply[event.timerId()]
        print("存在未回复的序列: ", data.seriaNum)


class Client(QObject):
    messageReceived = pyqtSignal(str)

    def __init__(self, socket: QWebSocket, parent=None):
        super(Client, self).__init__(parent)

        self.socket = socket
        self.socket.binaryMessageReceived.connect(self.handle_binary_message)

        self.keepAliveId = self.startTimer(5000)

        self.replyTrack = ReplyTrack()

    def send_keep_alive(self):
        data = SendData()
        data.seriaNum = generate_uuid()
        data.type = "action"
        data.action = "connection_check"
        self.send_command(data)

    def timerEvent(self, event):
        if event.timerId() == self.keepAliveId:
            self.send_keep_alive()

    def reply_online(self, received_data: SendData):
        data = SendData()
        data.seriaNum = received_data.seriaNum
        data.type = "reply"
        data.success = "true"
        data.action = "ready"
        data.message = bytes("成功", encoding="utf8")
        s = data.SerializeToString()
        if self.socket.sendBinaryMessage(s) != len(s):
            print("Send Data Error: ", data.seriaNum)

    def handle_binary_message(self, message):
        data = SendData()
        data.ParseFromString(message)

        print("收到: ", data.seriaNum, data.type, data.action, data.success, data.message.decode('utf8'))

        # 执行从client接收到的内容，并响应
        if data.HasField("ready") and data.type == "action" and data.action == "ready":
            self.messageReceived.emit(data.ready.currentMode + " " + str(data.ready.lon) + " " + str(data.ready.lat))
            self.reply_online(data)
        # 否则处理客户端响应服务端的内容
        else:
            self.messageReceived.emit(data.message.decode('utf8'))
            self.replyTrack.remove_track(data.seriaNum)

    def send_command(self, data: SendData):
        s = data.SerializeToString()
        if self.socket.sendBinaryMessage(s) == len(s):
            self.replyTrack.add_track(data)
        else:
            print("*****     ERROR     *****: ", data.seriaNum)
