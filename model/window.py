from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize


class BaseWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.initialize()
        self.setLayouts()

        self.setField()
        self.setWidget()

    def initialize(self):
        self.layout = QVBoxLayout()
        self.from_layout = QFormLayout()

    def setLayouts(self):
        self.layout.addLayout(self.from_layout)
        self.layout.addStretch(1)

        self.setLayout(self.layout)

    def setField(self):
        pass

    def setWidget(self):
        pass

    def addWidget(self, widget):
        self.layout.addWidget(widget)

    def addLayout(self, layout):
        self.layout.addLayout(layout)


class ToolBarMainWindow(QMainWindow):
    """
        QToolBar Main Window

        通过toolbar切换多层界面

        | button | button | button |
        ----------------------------
        |
        |     可切换界面
        |

    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("进进出出测试")
        self.tool_bar = QToolBar()
        self.main_widget = QStackedWidget()

        self.setLayouts()

    def setLayouts(self):
        self.tool_bar.setIconSize(QSize(32, 32))
        self.addToolBar(self.tool_bar)
        self.setCentralWidget(self.main_widget)

    def changeView(self, view):
        self.main_widget.removeWidget(self.main_widget.currentWidget())
        self.main_widget.addWidget(view)

    def addWindow(self, window, tag):
        action = QAction(tag, self)
        action.triggered.connect(lambda x, v=window: self.changeView(v))
        self.tool_bar.addAction(action)


class VerticalWidgetMainWindow(QMainWindow):
    """
        垂直控件 Main Window

        在垂直方向上，添加widget

        ----------------------
        |       widget        |
        -----------------------
        |       add widget1   | push
        -----------------------
        |      add widget2    | push
        -----------------------

    """

    class MainWidget(QWidget):

        def __init__(self, parent):
            super().__init__()

            self.initialize()
            self.setLayouts()

        def initialize(self):
            self.layout = QVBoxLayout()

        def setLayouts(self):
            self.setLayout(self.layout)

        def addWidget(self, widget):
            self.layout.addWidget(widget)

    def __init__(self):
        super().__init__()
        self.main_widget = self.MainWidget(self)
        self.setLayouts()

    def setLayouts(self):
        self.setCentralWidget(self.main_widget)

    def pushWidget(self, widget):
        self.main_widget.addWidget(widget)
