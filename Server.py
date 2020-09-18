from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtNetwork import QHostAddress
from PyQt5.QtWebSockets import QWebSocketServer

from Client import Client


class Server(QObject):
    new_client = pyqtSignal(Client)

    def __init__(self, address: str, port: int, parent=None):
        super(QObject, self).__init__(parent)

        self.address = address
        self.port = port
        self.isRunning = False
        self.webServer = None

        self.start_server()

    def new_connection(self):
        socket = self.webServer.nextPendingConnection()
        self.new_client.emit(Client(socket))

    def restart_server(self, address: str, port: int):
        print("Restart Server")
        self.webServer.close()
        self.isRunning = False
        self.address = address
        self.port = port
        self.start_server()

    def start_server(self):
        if self.isRunning:
            print("It is already running ...")
            return

        self.webServer = QWebSocketServer("Radar Server", QWebSocketServer.NonSecureMode)
        if self.webServer.listen(QHostAddress(self.address), self.port):
            self.isRunning = True
            print("Web Server Listen Success")
        else:
            print("Web Server Listen Error ...")
            return

        self.webServer.newConnection.connect(self.new_connection)
        self.webServer.serverError.connect(self.server_error)

    def server_error(self, close_code):
        socket = self.sender()
        print("Server Error: ", socket.peerAddress().toString(), socket.peerPort(), self.webServer.errorString())
