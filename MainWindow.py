from PyQt5.QtWidgets import QMainWindow

from ui.MainWindow import Ui_MainWindow

from Server import Server
from MessageCtrl import MessageCtrl
from ScanDevice import ScanDevice


class MainWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)

        self.ui.tabClients.setTabsClosable(True)
        self.ui.tabClients.tabCloseRequested.connect(self.tab_close_requested)

        self.scanDevice = ScanDevice()
        self.scanDevice.new_device.connect(self.ui.lwdScanResult.addItem)
        self.ui.cmbServiceIp.addItems(self.scanDevice.get_host_ip())
        self.ui.cmbServiceIp.currentIndexChanged.connect(self.scanDevice.set_current_index)

        self.server = Server(self.ui.cmbServiceIp.currentText(), int(self.ui.leServerPort.text()), self)
        self.server.new_client.connect(self.new_client)
        self.ui.btnRestartServer.clicked.connect(self.restart_server)

        self.ui.btnScanDevice.clicked.connect(self.scan_device)
        self.ui.lwdScanResult.itemDoubleClicked.connect(self.lwd_scan_result_double_clicked)

        self.__double_tag = None

    def new_client(self, client):
        tag = self.__double_tag
        if tag:
            index = self.find_tab(tag)
            if index == -1:
                message_ctrl = MessageCtrl(client)
                self.ui.tabClients.addTab(message_ctrl, self.__double_tag)
            else:
                message_ctrl = self.ui.tabClients.widget(index)
                message_ctrl.set_new_client(client)
            self.__double_tag = None

    def restart_server(self):
        self.clear_result()
        self.server.restart_server(self.ui.cmbServiceIp.currentText(), int(self.ui.leServerPort.text()))

    # 找到指定title，return index，否则return -1
    def find_tab(self, title):
        for index in range(self.ui.tabClients.count()):
            if self.ui.tabClients.tabText(index) == title:
                return index
        return -1

    def scan_device(self):
        self.ui.lwdScanResult.clear()
        self.scanDevice.search()

    def lwd_scan_result_double_clicked(self, item):
        tag = item.text()
        self.__double_tag = tag
        if self.find_tab(tag) == -1:
            self.scanDevice.connect_device(tag.split(":")[1])

    def close_tab(self, index):
        tag = self.ui.tabClients.tabText(index)
        self.scanDevice.disconnect_device(tag.split(":")[1])
        self.ui.tabClients.removeTab(index)

    def tab_close_requested(self, index):
        self.close_tab(index)

    def clear_result(self):
        self.ui.lwdScanResult.clear()
        count = self.ui.tabClients.count()
        for index in range(count):
            self.close_tab(0)

    def slot_test(self):
        print("XXOOXXOOXXOO")
