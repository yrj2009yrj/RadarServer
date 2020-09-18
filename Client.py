from PyQt5.QtCore import QObject
from PyQt5.QtWebSockets import QWebSocket


class Client(QObject):
    def __init__(self, socket: QWebSocket, parent=None):
        super(QObject, self).__init__(parent)

        self.socket = socket
