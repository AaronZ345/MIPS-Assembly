from PyQt5.QtWidgets import QTextBrowser
from PyQt5.QtGui import QFont


class Browser(QTextBrowser):
    def __init__(self):
        super(Browser, self).__init__()

        font = QFont('Consolas', 11)  # 设置窗口字体格式
        font.setFixedPitch(True)
        self.setFont(font)

        # 设置背景颜色与字体颜色
        self.setStyleSheet(
            'background-color: rgb(49, 48, 42);'
            'color: rgb(235, 229, 209);'
        )
