import re

from PyQt5.QtCore import QTimer, QThread
from model.window import *
from model.model import *
from workbox.httpposter import *
from classRoom import ClassRoom
from .execut.execut_add_user import async_addUser

import asyncio


class WorkThread(QThread):

    def __init__(self, parent):
        super().__init__()
        self.flag = False
        self.parent = parent

    def init(self, max_num, classRoom):
        self.max_num = max_num
        self.classroom = classRoom

    def run(self):
        self.flag = True
        asyncio.set_event_loop(asyncio.new_event_loop())
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.async_add_list())

        self.parent.setForbid(False)

    def my_stop(self):
        self.flag = False

    async def async_add_list(self):
        index = 0
        while self.flag and self.classroom.init_robot and index < self.max_num:
            vuser = self.classroom.init_robot.pop()
            await vuser.async_add_user(self.classroom.roomId)
            self.classroom.inroom_robot.append(vuser)
            index += 1

            if index % 10 == 0:
                time.sleep(0.1)


class ThreadStepAddWidget(BaseWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.worker = WorkThread(self.parent)
        self.classRoom = ClassRoom.singleton()

    def setField(self):
        self.user_num_spinbox_field = LineSpinBoxField(self, "载入人数", limit=999999, default=100)

    def start(self):
        self.max_num = self.user_num_spinbox_field.value()
        if self.max_num > self.classRoom.max_len:
            self.max_num = self.classRoom.max_len
        self.worker.init(self.max_num, self.classRoom)
        self.worker.start()

    def stop(self):
        self.worker.my_stop()


class StepAddWidget(BaseWidget):

    def __init__(self, parent):
        super().__init__()
        self.timer = QTimer(self)
        self.parent = parent
        self.timer.timeout.connect(self.add_user)
        self.classRoom = ClassRoom.singleton()

    def setField(self):
        self.user_num_spinbox_field = LineSpinBoxField(self, "载入总人数", default=100)
        self.step_num_spinbox_field = LineSpinBoxField(self, "每步载入的人数", limit=100)
        self.time_spinbox_field = LineSpinBoxField(self, "时间间隔(毫秒)", default=1000)

    def start(self):
        self.max_num = self.user_num_spinbox_field.value()
        self.step = self.step_num_spinbox_field.value()
        self.time = self.time_spinbox_field.value()

        if self.max_num > self.classRoom.max_len:
            self.max_num = self.classRoom.max_len

        self.timer.start(self.time)

    def add_user(self):
        inroom_robot_len = self.classRoom.get_inroom_robot_len()

        # 如果进入课程的机器人，已经大于或等于 设置的最大值后，停止计时器
        if inroom_robot_len >= self.max_num:
            self.timer.stop()
            self.parent.setForbid(False)

        # 当前已经在课程的机器人 + 下一次将要加入的机器人。如果将会大于 最大值
        # 调整step
        if (self.step + inroom_robot_len) >= self.max_num:
            step = self.max_num - inroom_robot_len
        else:
            step = self.step

        # 添加学生接口
        async_addUser(step,
                      self.classRoom)


class LinerAddWidget(BaseWidget):

    def __init__(self, parent):
        super().__init__()
        self.timer = QTimer(self)
        self.parent = parent
        self.timer.timeout.connect(self.add_user)
        self.classRoom = ClassRoom.singleton()

    def setField(self):
        self.user_num_spinbox_field = LineSpinBoxField(self, "载入总人数", default=100)
        self.start_num_spinbox_field = LineSpinBoxField(self, "起步人数", limit=100)
        self.add_num_spinbox_field = LineSpinBoxField(self, "增加幅度", limit=100)
        self.time_spinbox_field = LineSpinBoxField(self, "时间间隔(毫秒)", default=1000)

    def start(self):
        self.max_num = self.user_num_spinbox_field.value()
        self.start_num = self.start_num_spinbox_field.value()
        self.add_num = self.add_num_spinbox_field.value()
        self.time = self.time_spinbox_field.value()
        self.step = self.start_num

        if self.max_num > self.classRoom.max_len:
            self.max_num = self.classRoom.max_len

        self.timer.start(self.time)

    def stop(self):
        self.timer.stop()

    def add_user(self):
        inroom_robot_len = self.classRoom.get_inroom_robot_len()

        # 如果进入课程的机器人，已经大于或等于 设置的最大值后，停止计时器
        if inroom_robot_len >= self.max_num:
            self.timer.stop()
            self.parent.setForbid(False)

        # 线性递增中， 每次增加的都会叠加
        self.step += self.add_num

        # 当前已经在课程的机器人 + 下一次将要加入的机器人。如果将会大于 最大值
        # 调整step
        if (self.step + inroom_robot_len) >= self.max_num:
            step = self.max_num - inroom_robot_len
        else:
            step = self.step

        # 每一步不能超过100
        if step > 100:
            step = 100

        # 添加学生接口
        async_addUser(step,
                      self.classRoom)


class MiddleWidget(BaseWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.addMiddleWidget("逐步添加用户", StepAddWidget(self))
        # self.addMiddleWidget("线性递增添加用户", LinerAddWidget(self))
        self.addMiddleWidget("载入用户", ThreadStepAddWidget(self))
        self.classRoom = ClassRoom.singleton()

        self.flag = False

    def setWidget(self):
        self.addWidget(QLabel("选择用户加载方式:"))

        self.combo_box = QComboBox()
        self.combo_box.currentIndexChanged.connect(self.changeView)
        self.addWidget(self.combo_box)

        self.main_view = QStackedWidget()
        self.addWidget(self.main_view)

        self.start_button = QPushButton("开始载入")
        self.start_button.clicked.connect(self.start)
        self.addWidget(self.start_button)

    def start(self):
        if not self.classRoom.invest():
            QMessageBox.about(self, "提示", "未初始化课程")
            return

        if self.flag:
            self.main_view.currentWidget().stop()
            self.setForbid(not self.flag)
        else:
            self.main_view.currentWidget().start()
            self.setForbid(not self.flag)

    def setForbid(self, Flag=True):
        """
            设置自己禁止点击
        """
        self.flag = Flag
        if Flag:
            self.start_button.setText("停止载入")
            self.combo_box.setDisabled(True)
        else:
            self.start_button.setText("开始载入")
            self.combo_box.setDisabled(False)

    def changeView(self, index):
        self.main_view.setCurrentIndex(index)

    def addMiddleWidget(self, tag, view):
        self.combo_box.addItem(tag, view)
        self.main_view.addWidget(view)
