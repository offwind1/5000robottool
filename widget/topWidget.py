import re

from PyQt5.QtCore import QTimer
from model.window import *
from model.model import *
from workbox.httpposter import *
from classRoom import ClassRoom


class TopWidget(BaseWidget):

    def __init__(self):
        super().__init__()
        self.classRoom = ClassRoom.singleton()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_inroom_robot_label)
        self.timer.start(2000)

    def setField(self):
        self.code_text_field = TextEditField(self, "开课代码")

    def setWidget(self):
        self.start_button = QPushButton("获取课程信息，并初始化用户")
        self.start_button.clicked.connect(self.start)
        self.addWidget(self.start_button)

        self.group_id_label = QLabel()
        self.addWidget(self.group_id_label)

        self.teacher_accid_label = QLabel()
        self.addWidget(self.teacher_accid_label)

        self.robot_info_label = QLabel()
        self.addWidget(self.robot_info_label)

        self.inroom_robot_label = QLabel()
        self.addWidget(self.inroom_robot_label)

        self.hands_label = QLabel()
        self.addWidget(self.hands_label)

    def start(self):
        classCode = self.code_text_field.text()
        print(classCode)
        if classCode:
            self.classRoom.init(classCode)
            self.updateLabel()
        else:
            QMessageBox.about(self, '提示', '开课代码不能为空')

    def updateLabel(self, *__args):
        self.group_id_label.setText("课堂id:{}".format(self.classRoom.roomId))
        self.teacher_accid_label.setText("教室accid:{}".format(self.classRoom.tercherId))
        self.robot_info_label.setText("初始化机器人数量:{}".format(self.classRoom.get_init_robot_len()))

    def update_inroom_robot_label(self):
        self.inroom_robot_label.setText("已载入的机器人数量{}".format(self.classRoom.get_inroom_robot_len()))
        is_handing, no_handing = self.classRoom.get_hands_info()
        self.hands_label.setText("有{}学生正在举手".format(is_handing))