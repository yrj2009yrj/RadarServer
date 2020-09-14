from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow

from ui.MainWindow import Ui_MainWindow

from Server import Server

from protoc.SendData_pb2 import SendData, Ready


class MainWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)

        self.server = Server(self.ui.leServerAddress.text(), int(self.ui.leServerPort.text()), self)
        self.server.new_client_signal.connect(self.new_client)
        self.server.client_disconnected_signal.connect(self.client_disconnected)
        self.server.text_message_received_signal.connect(self.text_message_received)

        self.ui.btnRestartServer.clicked.connect(self.restart_server)

        # f = open(address_book_file, "rb")
        # address_book.ParseFromString(f.read())

        # ready = Ready()
        # ready.currentMode = "xxxx"
        # str = ready.SerializeToString()
        # print(str)
        # abc = Ready()
        # abc.ParseFromString(str)
        # print(abc.currentMode)

    def new_client(self, peer_address):
        self.ui.lwdClients.addItem(peer_address)
        print(peer_address + " Connected")

    def client_disconnected(self, peer_address):
        row = self.ui.lwdClients.row(self.ui.lwdClients.findItems(peer_address, Qt.MatchFixedString)[0])
        self.ui.lwdClients.takeItem(row)
        print(peer_address + " Disconnected")

    def restart_server(self):
        self.server.restart_server(self.ui.leServerAddress.text(), int(self.ui.leServerPort.text()))

    def text_message_received(self, message):
        self.ui.tbwDataReceived.append(message)

