from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtNetwork import QHostAddress, QUdpSocket


class ScanDevice(QObject):
    new_device = pyqtSignal(str)

    def __init__(self, parent=None):
        super(QObject, self).__init__(parent)

        self.udpSocket = QUdpSocket(self)
        self.udpSocket.readyRead.connect(self.data_received)

        self.__currentIndex = 0

    def set_current_index(self, index: int):
        self.__currentIndex = index

    def data_received(self):
        self.new_device.emit(str(self.udpSocket.receiveDatagram().data(), encoding="utf-8"))

    def get_host_ip(self):
        return ["192.168.3.21", "10.5.18.14"]

    # 广播服务器地址
    def search(self):
        ip = self.get_host_ip()[self.__currentIndex]
        if self.udpSocket.state() == QUdpSocket.UnconnectedState:
            self.udpSocket.bind(QHostAddress(ip), 60001)

        service_address = bytes("ws://" + self.get_host_ip()[self.__currentIndex] + ":8899", encoding="utf8")
        self.udpSocket.writeDatagram(b"PcCloudService-" + service_address, QHostAddress.Broadcast, 60000)

    # 告诉设备断开PC云服务，连接真实的云服务
    # 设备地址
    def disconnect_device(self, address):
        self.udpSocket.writeDatagram(b"ConnectToRealCloud-", QHostAddress(address), 60000)

    # 告诉设备连接PC云服务
    # 设备地址
    def connect_device(self, address):
        self.udpSocket.writeDatagram(b"ConnectToPcCloud-", QHostAddress(address), 60000)
