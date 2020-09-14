from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWebSockets import QWebSocketServer
from PyQt5.QtNetwork import QHostAddress


class Server(QObject):
    new_client_signal = pyqtSignal(str)
    client_disconnected_signal = pyqtSignal(str)
    text_message_received_signal = pyqtSignal(str)

    def __init__(self, address, port, parent=None):
        super(QObject, self).__init__(parent)

        self.client = {}
        self.isRunning = False
        self.address = address
        self.port = port
        self.webServer = None

        self.start_server()

    def new_connection(self):
        new_client = self.webServer.nextPendingConnection()
        peer_address_port = new_client.peerAddress().toString()+":"+str(new_client.peerPort())
        self.new_client_signal.emit(peer_address_port)
        self.client[peer_address_port] = new_client


        # new_client.binaryMessageReceived.connect(self.client_disconnected)
        new_client.textMessageReceived.connect(self.text_message_received)

        new_client.disconnected.connect(self.client_disconnected)

    def text_message_received(self, message):
        client = self.sender()
        peer_address_port = client.peerAddress().toString() + ":" + str(client.peerPort())
        self.text_message_received_signal.emit(peer_address_port + " " + message)



    def client_disconnected(self):
        client = self.sender()
        peer_address_port = client.peerAddress().toString()+":"+str(client.peerPort())
        del self.client[peer_address_port]
        self.client_disconnected_signal.emit(peer_address_port)

    def restart_server(self, address, port):
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

        self.webServer.newConnection.connect(self.new_connection)
        self.webServer.serverError.connect(self.server_error)

    def server_error(self, close_code):
        web_socket = self.sender()
        print("Server Error: ", web_socket.peerAddress().toString(),
              web_socket.peerPort(), self.webServer.errorString())
