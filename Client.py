from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWebSockets import QWebSocket

from protoc.SendData_pb2 import SendData

import uuid


class Client(QObject):
    messageReceived = pyqtSignal(str)

    def __init__(self, socket: QWebSocket, parent=None):
        super(Client, self).__init__(parent)

        self.socket = socket
        self.socket.binaryMessageReceived.connect(self.handle_binary_message)

        self.keepAliveId = self.startTimer(5000)

        self.serialTrack = []

    def send_keep_alive(self):
        data = SendData()
        data.seriaNum = ''.join(str(uuid.uuid4()).split('-'))
        data.type = "action"
        data.action = "connection_check"
        s = data.SerializeToString()
        if self.socket.sendBinaryMessage(s) == len(s):
            self.serialTrack.append(data.seriaNum)
        else:
            print("Send Data Error: ", data.seriaNum)

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
        pass

    def handle_binary_message(self, message):
        data = SendData()
        data.ParseFromString(message)

        print(data.seriaNum, data.type, data.action, data.success, data.message.decode('utf8'))

        if data.HasField("ready") and data.type == "action" and data.action == "ready":
            self.messageReceived.emit(data.ready.currentMode + " " + str(data.ready.lon) + " " + str(data.ready.lat))
            self.reply_online(data)
        else:
            self.messageReceived.emit(data.message.decode('utf8'))

        self.serialTrack.remove(data.seriaNum) if data.seriaNum in self.serialTrack else None
        if self.serialTrack:
            print("存在未回复的序列: ", len(self.serialTrack))



