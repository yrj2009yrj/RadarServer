from PyQt5.QtWidgets import QWidget, QTextBrowser, QPushButton, QVBoxLayout


class MessageCtrl(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()

        self.tbwMessage = QTextBrowser(self)
        self.btnClean = QPushButton("clean", self)
        self.btnClean.clicked.connect(self.clean_message)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.tbwMessage)
        self.layout.addWidget(self.btnClean)

    def append(self, text):
        self.tbwMessage.append(text)

    def clean_message(self):
        self.tbwMessage.clear()

