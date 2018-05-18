from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QMessageBox, QMenu, QDockWidget
from Assembler import Assembler
from Editor import Editor
from Browser import Browser


# 主窗口对象
class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.setWindowTitle('MIPS')  # 窗口标题

        # 设置各项菜单
        self.setupFileMenu()
        self.setupAssembleMenu()
        self.setupDebugMenu()
        self.setupHelpMenu()

        self.setupEditor()  # 设置编辑器
        self.setCentralWidget(self.editor)

        self.setupDock()  # 设置Dock栏

    def setupEditor(self):
        self.editor = Editor()  # 创建编辑器对象

    def setupFileMenu(self):
        fileMenu = QMenu('文件(&F)', self)
        self.menuBar().addMenu(fileMenu)

        self.currentFile = ''  # 设置当前文件路径为空值

        fileMenu.addAction('新建(&N)', self.newFile, 'Ctrl+N')  # 新建立一个文件
        fileMenu.addAction('打开(&O)...', self.openFile, 'Ctrl+O')  # 打开已有的文件
        fileMenu.addAction('保存(&S)', self.saveFile, 'Ctrl+S')  # 将当前文件保存
        fileMenu.addAction('另存为(&A)...', self.saveAnotherFile, 'Ctrl+Alt+S')  # 将当前文件保存到指定路径
        fileMenu.addAction('退出(&X)', self.close, 'Ctrl+F4')  # 退出MIPS汇编器

    def setupAssembleMenu(self):
        assembleMenu = QMenu('汇编(&A)', self)
        self.menuBar().addMenu(assembleMenu)

        self.assembler = Assembler()  # 创建汇编器对象

        assembleMenu.addAction('汇编(&A)', self.assemble, 'F10')  # 对当前代码实行汇编操作
        assembleMenu.addAction('反汇编(&D)', self.disassemble, 'F11')  # 对当前代码实行反汇编操作

    def setupDebugMenu(self):
        assembleMenu = QMenu('调试(&D)', self)
        self.menuBar().addMenu(assembleMenu)

        self.isStart = False  # 设置是否开始调试布尔值为否

        assembleMenu.addAction('启动调试(&S)', self.startDebug, 'F5')  # 启动调试
        assembleMenu.addAction('继续调试(&C)', self.contiuneDebug, 'F5')  # 将调试进行到最后一步
        assembleMenu.addAction('单步执行(&I)', self.nextDebug, 'F11')  # 单步进行调试
        assembleMenu.addAction('停止调试(&S)', self.stopDebug, 'Shift+F5')  # 停止调试过程
        assembleMenu.addAction('重启调试(&R)', self.resetDebug, 'Ctrl+Shift+F5')  # 重新启动调试过程

    def setupHelpMenu(self):
        helpMenu = QMenu("帮助(&H)", self)
        self.menuBar().addMenu(helpMenu)

        helpMenu.addAction('关于(&A)', self.about)  # 本程序的小介绍

    def setupDock(self):
        # 建立输出运行结果的窗口
        self.rightBrowser = Browser()  # 建立在窗口右端
        self.rightDock = QDockWidget('运行结果/内存', self)
        self.rightDock.setFeatures(QDockWidget.DockWidgetClosable)
        self.rightDock.setWidget(self.rightBrowser)
        self.addDockWidget(Qt.RightDockWidgetArea, self.rightDock)
        self.rightDock.hide()  # 窗口自动隐藏

        # 建立输出调试过程的窗口
        self.bottomBrowser = Browser()  # 建立在窗口底端
        self.bottomDock = QDockWidget('调试窗口', self)
        self.bottomDock.setFeatures(QDockWidget.DockWidgetClosable)
        self.bottomDock.setWidget(self.bottomBrowser)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.bottomDock)
        self.bottomDock.hide()

    def newFile(self):
        self.editor.clear()  # 清空当前屏幕
        self.rightDock.hide()  # 隐藏Dock栏
        self.bottomDock.hide()
        self.currentFile = ''
        return True

    def openFile(self):
        # 打开汇编文件或二进制文件
        path, _ = QFileDialog.getOpenFileName(
            self, '打开', '',
            '汇编文件 (*.asm);;二进制文件(*.coe *.bin)'
            )

        if path:
            file = open(path, 'r')
            self.editor.setPlainText(file.read())
            file.close()

            self.rightDock.hide()
            self.bottomDock.hide()

            self.currentFile = path
            return True

        return False

    def saveFile(self):
        # 如果没有文件名则跳转到另存为
        if not self.currentFile:
            return self.saveAnotherFile()

        # 将编辑器内容写入到当前路径文件
        file = open(self.currentFile, 'w')
        file.write(self.editor.toPlainText())
        file.close()

        return True

    def saveAnotherFile(self):
        # 选择存入文件路径
        path, _ = QFileDialog.getSaveFileName(
            self, '另存为', self.currentFile if self.currentFile else '',
            '汇编文件 (*.asm);;二进制文件(*.coe *.bin)'
            )

        # 路径存在则将编辑器内容写入
        if path:
            file = open(path, 'w')
            file.write(self.editor.toPlainText())
            file.close()

            self.currentFile = path
            return True

        return False

    def assemble(self):
        self.saveFile()  # 执行前保存文件

        try:
            self.rightBrowser.setText(self.assembler.assembly(self.currentFile))  # 执行汇编并在右侧输出结果
        except:
            self.rightBrowser.setText('error!!! \ncheck your code!!!')  # 代码有误不能正确汇编
        return self.rightDock.show()

    def disassemble(self):
        self.saveFile()

        try:
            self.rightBrowser.setText(self.assembler.disassembly(self.currentFile))  # 执行反汇编并在右侧输出结果
        except:
            self.rightBrowser.setText('error!!! \ncheck your code!!!')  # 代码有误不能正确反汇编
        return self.rightDock.show()

    def startDebug(self):
        self.saveFile()

        self.assembler.step = 0  # 初始化执行步数
        self.debugStr = ''  # 初始化结果字符
        self.isStart = True  # 设定已经开始

        # 初始化寄存器内容
        for k in self.assembler.registers:
            self.assembler.registers[k] = '00000000'
        self.assembler.memory = {}  # 初始化内存

        try:
            self.assembler.debug(self.currentFile)
            self.debugStr = str(self.assembler.memory).strip("{}").replace("'", '').replace(':', ' ').replace(',', ' ')  # 执行单步模拟操作
        except:
            self.debugStr += '\nthe debug is over\nnow check your code'  # 模拟完成或代码有误则停止
            return False

        # 将寄存器内容展示在底部，结果展示在右部
        self.bottomBrowser.setText(' ' + str(self.assembler.registers).strip("{},").replace(':', '\t').replace(',', '\t').replace("'", ''))
        self.rightBrowser.setText(self.debugStr)
        self.rightDock.show()
        self.bottomDock.show()
        return True

    def contiuneDebug(self):
        # 如果没有开始则开始调试
        if not self.isStart:
            self.startDebug()

        # 模拟进行到最后一步
        while self.nextDebug():
            continue

        self.bottomBrowser.setText(str(self.assembler.registers).strip("{},").replace(':', '\t').replace(',', '\t').replace("'", ''))
        self.rightBrowser.setText(self.debugStr)
        self.rightDock.show()
        self.bottomDock.show()
        return True

    def nextDebug(self):
        if not self.isStart:
            return self.startDebug()

        try:
            self.assembler.debug(self.currentFile)
            self.debugStr = str(self.assembler.memory).strip("{}").replace("'", '').replace(':', ' ').replace(',', ' ')
        except:
            self.debugStr += '\nthe debug is over\nnow check your code'
            self.rightBrowser.setText(self.debugStr)
            self.rightDock.show()
            return False

        self.bottomBrowser.setText(str(self.assembler.registers).strip("{},").replace(':', '\t').replace(',', '\t').replace("'", ''))
        self.rightBrowser.setText(self.debugStr)
        self.rightDock.show()
        self.bottomDock.show()
        return True

    def stopDebug(self):
        self.isStart = False  # 结束调试并将开始置否
        self.bottomDock.hide()
        self.rightDock.hide()
        return True

    def resetDebug(self):
        self.stopDebug()
        return self.startDebug()

    def about(self):
        # 简短介绍本程序
        QMessageBox.about(
            self, '关于本MIPS汇编器',
            '<p style="font-size: 16px;">Made By Aaron</p>'
            '<p style="font-size: 16px;">可实现MIPS汇编器（支持伪码），反汇编器，调试器</p>'
            '<p style="font-size: 16px;">介绍请见README.md</p>'
            '<p style="font-size: 16px;">具体细节请参考实验报告'
        )
