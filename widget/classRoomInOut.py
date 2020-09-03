import re

from model.window import *
from model.model import *
from workbox.httpposter import *
import threading





#
#
# class ClassRoomInOut(BaseWidget):
#
#     def __init__(self, *arg, **kwargs):
#         super().__init__(*arg, **kwargs)
#
#         self.roomid = ""  # 聊天室组id
#         self.teacherid = ''  # 教室accid
#
#         self.init_accids = []
#         self.in_room_accids = []
#
#     def setField(self):
#         self.code_text_field = TextEditField(self, "开课代码")
#
#         self.add_button_field = ButtonSpinBoxField(self, "加入用户数量", self.addUser)
#         self.remove_button_field = ButtonSpinBoxField(self, "退出用户数量", self.removeUser)
#
#         self.handsup_button_field = ButtonSpinBoxField(self, "举手", self.handsup)
#         self.handsdown_button_field = ButtonSpinBoxField(self, "取消举手", self.handsdown)
#
#     def setWidget(self):
#
#
#
#         self.initUserLabel = QLabel()
#         self.addWidget(self.initUserLabel)
#
#         self.inRoomUserLabel = QLabel()
#         self.addWidget(self.inRoomUserLabel)
#
#         self.handingInfoLabel = QLabel()
#         self.addWidget(self.handingInfoLabel)
#
#         self.load_button = QPushButton("载入虚拟用户")
#         self.load_button.clicked.connect(self.load)
#         self.addWidget(self.load_button)
#
#     def getRoomid(self):
#         code = self.code_text_field.text()
#         if code:
#             self.roomid, self.teacherid = getCloudGroupId(code)
#
#     def load(self):
#         self.init_accids.clear()
#         self.in_room_accids.clear()
#
#         self.getRoomid()
#         loadAccids(self.init_accids)
#         self.updateLabel()
#
#     def addUser(self):
#         if not self.roomid:
#             return
#
#         addUser(self.add_button_field.value(), self.roomid, self.init_accids, self.in_room_accids)
#         self.updateLabel()
#
#     def removeUser(self):
#         if not self.roomid:
#             return
#
#         remove(self.remove_button_field.value(), self.roomid, self.init_accids, self.in_room_accids)
#         self.updateLabel()
#
#     def initialize_user(self):
#         initAccids(self.initialize_button_field.value())
#         self.updateLabel()
#
#     def updateLabel(self):
#         self.initUserLabel.setText("虚拟用户数{}".format(len(self.init_accids)))
#         self.inRoomUserLabel.setText("进入课程的用户数{}".format(len(self.in_room_accids)))
#
#     def updateHandsLabel(self):
#         is_handing = 0
#         no_handing = 0
#
#         for vu in self.in_room_accids:
#             if vu.is_handing == False:
#                 no_handing += 1
#             elif vu.is_handing == True:
#                 is_handing += 1
#
#         self.handingInfoLabel.setText("有{}学生正在举手".format(is_handing))
#
#     def handsup(self):
#         if not self.roomid:
#             return
#
#         t = threading.Thread(target=handsup, args=(self.handsup_button_field.value(),
#                                                    self.in_room_accids,
#                                                    self.roomid,
#                                                    self.teacherid,
#                                                    self.updateHandsLabel))
#         t.start()
#
#     def handsdown(self):
#         if not self.roomid:
#             return
#         t = threading.Thread(target=handsdown, args=(self.handsdown_button_field.value(),
#                                                      self.in_room_accids,
#                                                      self.roomid,
#                                                      self.teacherid,
#                                                      self.updateHandsLabel))
#         t.start()
#
#
# def handsup(num, in_room_accids, roomid, teacherid, func):
#     list = []
#     for vu in in_room_accids:
#         if vu.is_handing == False:
#             list.append(vu)
#
#     random.shuffle(list)
#
#     if num > len(list):
#         num = len(list)
#
#     for i in range(num):
#         vuser = list.pop()
#         vuser.userHandsup(roomid, teacherid)
#
#     func()
#
#
# def handsdown(num, in_room_accids, roomid, teacherid, func):
#     list = []
#     for vu in in_room_accids:
#         if vu.is_handing == True:
#             list.append(vu)
#
#     if num > len(list):
#         num = len(list)
#
#     for i in range(num):
#         vuser = list.pop()
#         vuser.userHandsdown(roomid, teacherid)
#
#     func()
