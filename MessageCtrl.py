from PyQt5.QtWidgets import QWidget, QTextBrowser, QHBoxLayout, QPushButton, QVBoxLayout, QLabel, QTabWidget
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import pyqtSignal, QTimer
from PyQt5.QtChart import QChart, QChartView, QLineSeries

from ui.ControlTab import Ui_ControlTab

from protoc.SendData_pb2 import SendData, Collect

from Client import Client
from Utils import *


class ControlTab(QWidget):
    def __init__(self):
        super(ControlTab, self).__init__()
        self.ui = Ui_ControlTab()
        self.ui.setupUi(self)
        self.ui.btnExecute.clicked.connect(self.execute_command)
        self.ui.btnAdd.clicked.connect(self.add_action)
        self.ui.btnClear.clicked.connect(self.clear_action)

        self.client = None

        self.partLists = []

    @property
    def h_angle(self):
        return self.ui.spnHAngle.value()

    @property
    def v_angle(self):
        return self.ui.spnVAngle.value()

    @property
    def s_angle(self):
        return self.ui.spnSAngle.value()

    @property
    def e_angle(self):
        return self.ui.spnEAngle.value()

    @property
    def i_angle(self):
        return self.ui.spnIAngle.value()

    @property
    def i_time(self):
        return self.ui.spnITime.value()

    @property
    def stop_type(self):
        return self.ui.cmbStopType.currentIndex()

    @property
    def stop_condition_value(self):
        return self.ui.spnConditionValue.value()

    @property
    def collect_mode(self):
        return self.ui.cmbCollectMode.currentText()

    def execute_command(self):
        data = SendData()
        data.seriaNum = generate_uuid()
        data.type = "action"
        data.action = "collect"
        collect = data.collect
        if self.partLists:
            collect.collectMode = "custom" if len(self.partLists) > 1 else self.collect_mode
        else:
            return

        self.client.send_command(data)

    def add_action(self):
        self.partLists.append((self.h_angle, self.v_angle, self.s_angle, self.e_angle,
                               self.i_angle, self.i_time, self.collect_mode, self.stop_condition_value))
        self.ui.lwdActionList.addItem(str(len(self.partLists)-1))

    def clear_action(self):
        self.ui.lwdActionList.clear()
        self.partLists.clear()



class ChartWidget(QWidget):
    def __init__(self, number: int, parent=None):
        super(QWidget, self).__init__(parent)

        self.layout = QVBoxLayout(self)

        self.chart = QChart()
        self.chartView = QChartView(self.chart)
        self.chartView.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
        self.layout.addWidget(self.chartView)

        self.channelNumber = number
        for index in range(self.channelNumber):
            tmp = QLineSeries()
            tmp.setName("channel "+str(index))
            self.chart.addSeries(tmp)

        self.chart.createDefaultAxes()
        self.chart.axisX().setRange(0, 25)
        self.chart.axisX().setTitleText("AAA")
        self.chart.axisY().setRange(0, 25)
        self.chart.axisY().setTitleText("BBB")

        # 标题
        self.chart.setTitle("XXX XXX XXX")
        # 指示颜色所代表的内容
        # self.chart.legend().hide()
        # 动画效果
        self.chart.setAnimationOptions(QChart.AllAnimations)

    def set_line(self, *lines):
        for index in range(len(lines)):
            self.chart.series()[index].clear()
            for v1, v2 in enumerate(lines[index]):
                self.chart.series()[index].append(v1, v2)


class MessageCtrl(QWidget):
    def __init__(self, client: Client, parent=None):
        super(QWidget, self).__init__(parent)

        self.layout = QVBoxLayout(self)
        self.tbwShow = QTabWidget(self)
        self.tbwShow.setTabPosition(QTabWidget.West)
        self.layout.addWidget(self.tbwShow)

        self.tbwMessage = QTextBrowser()
        self.lblState = QLabel()
        self.btnClean = QPushButton("clean")
        self.btnClean.clicked.connect(self.clean_message)

        self.wdtTab1 = QWidget()
        self.tbwShow.addTab(self.wdtTab1, "tab1")
        self.wdtTab2 = QWidget()
        self.tbwShow.addTab(self.wdtTab2, "tab2")
        self.wdtTab3 = ControlTab()
        self.tbwShow.addTab(self.wdtTab3, "tab3")

        self.layout1 = QVBoxLayout(self.wdtTab1)
        self.layout1.addWidget(self.tbwMessage)
        self.layout2 = QHBoxLayout()
        self.layout1.addLayout(self.layout2)
        self.layout2.addWidget(self.lblState)
        self.layout2.addWidget(self.btnClean)

        self.client = None
        self.set_new_client(client)

        self.layout3 = QVBoxLayout(self.wdtTab2)

        self.chartWidget = ChartWidget(4)
        self.layout3.addWidget(self.chartWidget)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timer_timeout)
        self.timer.start(1000)

        self.line1 = [1,  2,  3,  4,  5,  6 ]
        self.line2 = [2,  4,  6,  8,  10, 12]
        self.line3 = [3,  6,  9,  12, 15, 18]
        self.line4 = [4,  8,  12, 16, 20, 24]
        self.line5 = [6,  5,  4,  3,  2,  1]
        self.line6 = [12, 10, 8,  6,  4,  2]
        self.line7 = [18, 15, 12, 9,  6,  3]
        self.line8 = [24, 20, 16, 12, 8,  4]
        self.showFlag = True

    def clean_message(self):
        self.tbwMessage.clear()

    def message_received(self, message):
        peer_ip_port = self.client.socket.peerAddress().toString() + ":" + str(self.client.socket.peerPort())
        self.tbwMessage.append(peer_ip_port + " " + message)

    def client_disconnected(self):
        peer_ip_port = self.client.socket.peerAddress().toString() + ":" + str(self.client.socket.peerPort())
        print(peer_ip_port + " Disconnected")
        # 清理 self.client 和 self.wdtTab3.client
        self.client = None
        self.wdtTab3.client = None
        self.lblState.setText("offline")

    def set_new_client(self, client: Client):
        self.client = client
        self.wdtTab3.client = client
        self.client.messageReceived.connect(self.message_received)
        self.client.socket.disconnected.connect(self.client_disconnected)
        self.lblState.setText("online")

    def timer_timeout(self):
        # 更改坐标轴的最大值
        if self.showFlag:
            self.chartWidget.set_line(self.line1, self.line2, self.line3, self.line4)
            self.showFlag = False
        else:
            self.chartWidget.set_line(self.line5, self.line6, self.line7, self.line8)
            self.showFlag = True

        pass
