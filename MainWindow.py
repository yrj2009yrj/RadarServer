from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow

from ui.MainWindow import Ui_MainWindow

from Server import Server
from MessageCtrl import MessageCtrl

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
        self.ui.lwdClients.itemDoubleClicked.connect(self.client_double_clicked)

        # key：字符串title
        # value: 实例类MessageCtrl()
        self.clients = {}

        # itemDoubleClicked(QListWidgetItem * item)

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

    def client_disconnected(self, peer_address_port):
        row = self.ui.lwdClients.row(self.ui.lwdClients.findItems(peer_address_port, Qt.MatchFixedString)[0])
        self.ui.lwdClients.takeItem(row)
        index = self.find_tab(peer_address_port)
        self.remove_tab(index) if index >= 0 else None
        print(peer_address_port + " Disconnected")

    def restart_server(self):
        self.server.restart_server(self.ui.leServerAddress.text(), int(self.ui.leServerPort.text()))

    def text_message_received(self, peer_address_port, message):
        if peer_address_port in self.clients.keys():
            self.clients[peer_address_port].append(peer_address_port + " " + message)

    def client_double_clicked(self, item):
        title = item.text()
        index = self.find_tab(title)

        # 发现就删除
        if index >= 0:
            self.ui.tabClients.removeTab(index)
            del self.clients[title]
            return

        # 没发现就增加
        message_ctrl = MessageCtrl()
        self.clients[title] = message_ctrl
        self.ui.tabClients.addTab(message_ctrl, title)

    # 找到指定title，return index，否则return -1
    def find_tab(self, title):
        for index in range(self.ui.tabClients.count()):
            if self.ui.tabClients.tabText(index) == title:
                return index
        return -1

    def remove_tab(self, index):
        del self.clients[self.ui.tabClients.tabText(index)]
        self.ui.tabClients.removeTab(index)

