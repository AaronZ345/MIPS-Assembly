from PyQt5.QtCore import Qt, QSize, QRect
from PyQt5.QtGui import QFont, QColor, QPainter, QTextFormat
from PyQt5.QtWidgets import QWidget, QTextEdit, QPlainTextEdit


# 继承小部件建立行号区域类
class LineNumber(QWidget):

    def __init__(self, parent):
        super(LineNumber, self).__init__(parent)
        self.editor = parent

    def paintEvent(self, event):
        self.editor.lineNumberAreaPaintEvent(event)


class Editor(QPlainTextEdit):
    def __init__(self):
        super(Editor, self).__init__()

        font = QFont('Consolas', 11)  # 设置编辑器字体格式
        font.setFixedPitch(True)

        self.setFont(font)

        # 设置背景颜色与字体颜色
        self.setStyleSheet(
            'background-color: rgb(49, 48, 42);'
            'color: rgb(235, 229, 209);'
        )

        self.setLineWrapMode(QPlainTextEdit.NoWrap)  # 设置不自动换行
        self.setTabStopWidth(40)  # 设置Tab间距

        self.lineNumber = LineNumber(self)

        self.updateRequest.connect(self.updateArea)  # 段落变化时调用updateArea函数
        self.cursorPositionChanged.connect(self.lightCurrent)  # 当前行变化时调用lightCurrent函数

        self.setViewportMargins(40, 0, 0, 0)  # 设置行号区域大小

    def updateArea(self, rect):
        self.lineNumber.update(0, rect.y(), 40, rect.height())  # 根据变化调整矩形

    # 监听变化并调整矩形
    def resizeEvent(self, event):
        self.lineNumber.setGeometry(
            QRect(self.contentsRect().left(), self.contentsRect().top(), 40, self.contentsRect().height())
        )

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumber)

        font = QFont('Consolas', 11)
        font.setFixedPitch(True)

        painter.setFont(font)
        painter.setPen(QColor(235, 229, 209))

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()

        # 计算行号的头部和底部位置
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        height = self.fontMetrics().height()

        # 对每一个可见的行进行行号标示
        while block.isValid():
            if block.isVisible():
                painter.drawText(
                    0, top, 40, height,
                    Qt.AlignCenter, (str(blockNumber + 1) + ' ').rjust(4)
                )

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1

    def lightCurrent(self):
        extraSelections = []

        selection = QTextEdit.ExtraSelection()

        selection.format.setBackground(QColor(78, 80, 76))
        selection.format.setProperty(QTextFormat.FullWidthSelection, True)
        selection.cursor = self.textCursor()
        selection.cursor.clearSelection()
        extraSelections.append(selection)

        # 为当前行设置新的显示方式
        self.setExtraSelections(extraSelections)
