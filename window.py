import sys
from PyQt5.QtWidgets import QApplication
from model.window import *
from widget import *
from model.model import *

#
# class Window(ToolBarMainWindow):
#     def __init__(self):
#         super().__init__()
#
#         self.addWindow(ClassRoomInOut(), "用户进出检查")
#         self.addWindow(ClassRoomAuto(), "自动进出")


class VerWindow(VerticalWidgetMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("云课机器人负载测试工具")
        self.resize(500, 500)

        self.topWidget = TopWidget()
        self.middleWidget = MiddleWidget()
        self.bottomWidget = BottomWidget()

        self.pushWidget(self.topWidget)
        self.pushWidget(self.middleWidget)
        self.pushWidget(self.bottomWidget)


def start2():
    app = QApplication(sys.argv)
    window = VerWindow()
    window.show()
    sys.exit(app.exec_())

#
# def start1():
#     app = QApplication(sys.argv)
#     window = Window()
#     window.show()
#     sys.exit(app.exec_())
#

if __name__ == '__main__':
    start2()
