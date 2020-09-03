from PyQt5.QtCore import QThread, QTimer
from model.model import *
from classRoom import ClassRoom
import time

from widget.execut.execut_add_user import AddUser
from widget.execut.execut_remove_user import RemoveUser
from widget.execut.execut_hands_up import HandsUp
from widget.execut.execut_hands_down import HandsDown
from widget.execut.execut_send_danmu import SendDanmu
from widget.execut.execut_send_text import SendText


class ExecuteWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.flag = True
        self.temp_func = None
        self.classRoom = ClassRoom.singleton()

        self.worker = None

        self.initialize()
        self.setStyle()
        self.setConfig()
        self.setLayouts()
        self.setExecut()

    def initialize(self):
        self.time_label = QLabel("时间")
        self.time_spinbox = QSpinBox()
        self.execut_cb = QComboBox()
        self.step_spinbox = QSpinBox()
        self.start_button = QPushButton("执行")

        self.timer = QTimer()

    def setStyle(self):
        self.setContentsMargins(0, 0, 0, 0)
        self.time_spinbox.setMinimum(1)
        self.time_spinbox.setMaximum(99999)
        self.time_spinbox.setValue(1000)

        self.step_spinbox.setMaximum(100)
        self.step_spinbox.setMinimum(1)

    def addExecut(self, execut):
        self.execut_cb.addItem(execut.name, execut)

    def setConfig(self):
        self.start_button.clicked.connect(self.start)

    def setExecut(self):
        self.addExecut(AddUser)
        self.addExecut(RemoveUser)
        self.addExecut(HandsUp)
        self.addExecut(HandsDown)
        self.addExecut(SendDanmu)
        self.addExecut(SendText)

    def setLayouts(self):
        layout = QHBoxLayout()
        layout.addWidget(self.time_label)
        layout.addWidget(self.time_spinbox)
        layout.addWidget(self.execut_cb)
        layout.addWidget(self.step_spinbox)
        layout.addWidget(self.start_button)

        self.setLayout(layout)


    def _setForbid(self, Flag=True):
        """
            设置自己禁止点击
        """
        if Flag:
            self.start_button.setText("停止")
            self.execut_cb.setDisabled(True)
        else:
            self.start_button.setText("执行")
            self.execut_cb.setDisabled(False)


    def start(self):
        if not self.classRoom.invest():
            QMessageBox.about(self, "提示", "未初始化课程")
            return

        if self.worker is None or not self.worker.flag:
            # 开始
            clazz = self.execut_cb.currentData()
            if callable(clazz):
                self.worker = clazz()
            else:
                raise Exception("有问题")

            time = self.time_spinbox.value()
            step = self.step_spinbox.value()

            self.worker.start(time, step, self.classRoom)
            self._setForbid(True)
        elif self.worker.flag and self.worker:
            # 结束
            self.worker.stop()
            self._setForbid(False)

