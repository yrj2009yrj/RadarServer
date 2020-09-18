from PyQt5.QtWidgets import QWidget, QTextBrowser, QPushButton, QVBoxLayout

from Client import Client


class MessageCtrl(QWidget):
    def __init__(self, client: Client, parent=None):
        super(QWidget, self).__init__(parent)

        self.tbwMessage = QTextBrowser(self)
        self.btnClean = QPushButton("clean", self)
        self.btnClean.clicked.connect(self.clean_message)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.tbwMessage)
        self.layout.addWidget(self.btnClean)

        self.client = None
        self.set_new_client(client)

    def clean_message(self):
        self.tbwMessage.clear()

    def text_message_received(self, message):
        peer_ip_port = self.client.socket.peerAddress().toString() + ":" + str(self.client.socket.peerPort())
        self.tbwMessage.append(peer_ip_port + " " + message)

    def client_disconnected(self):
        peer_ip_port = self.client.socket.peerAddress().toString() + ":" + str(self.client.socket.peerPort())
        print(peer_ip_port + " Disconnected")
        self.client = None

    def set_new_client(self, client: Client):
        self.client = client
        self.client.socket.textMessageReceived.connect(self.text_message_received)
        self.client.socket.disconnected.connect(self.client_disconnected)

