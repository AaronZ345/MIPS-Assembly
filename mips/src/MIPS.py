import sys
from PyQt5.QtWidgets import QApplication
from Window import Window


# 主函数
def main():
    app = QApplication(sys.argv)  # 创建QApplication对象获取命令行参数
    window = Window()  # 建立一个新窗口
    window.resize(960, 640)  # 设定窗口大小
    window.show()  # 展示窗口
    sys.exit(app.exec_())  # 退出程序


main()
