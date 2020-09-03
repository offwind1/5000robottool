import re

from model.window import *
from model.model import *
from workbox.httpposter import *
import threading
import time as timeing

io_auto = False
hands_auto = False

#
# class ClassRoomAuto(BaseWidget):
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
#         self.time_text_field = LineSpinBoxField(self, "毫秒", default=2000, limit=900000)
#
#         self.step_button_field = ButtonSpinBoxField(self, "逐步加入用户", self.stepAddUser, limit=100)
#         self.line_button_field = ButtonSpinBoxField(self, "线性添加用户", self.lineAddUser, limit=100)
#
#         self.autoio_button_field = ButtonSpinBoxField(self, "自动进出:  浮动值", self.auto_io, limit=100)
#
#         self.remove_button_field = ButtonSpinBoxField(self, "退出用户数量", self.removeUser, limit=100)
#
#         # self.handsup_button_field = ButtonSpinBoxField(self, "举手", self.handsup, limit=100)
#         # self.handsdown_button_field = ButtonSpinBoxField(self, "取消举手", self.handsdown, limit=100)
#
#         self.hansauto_button_field = ButtonSpinBoxField(self, "自动举手", self.handsauto, limit=100)
#
#     def setWidget(self):
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
#     def setAddButtonDisabled(self, flag):
#         self.line_button_field.setDisabled(flag)
#         self.step_button_field.setDisabled(flag)
#
#     def auto_io(self):
#         global io_auto
#
#         if io_auto == False:
#             time = self.time_text_field.value()
#             step = self.autoio_button_field.value()
#
#             io_auto = True
#
#             t = threading.Thread(target=auto_io,
#                                  args=(time,
#                                        step,
#                                        self.roomid,
#                                        self.init_accids,
#                                        self.in_room_accids,
#                                        self.updateLabel))
#             t.start()
#
#             self.autoio_button_field.updateButtonText("停止自动用户进出")
#
#         elif io_auto == True:
#             io_auto = False
#             self.autoio_button_field.updateButtonText("自动进出:  浮动值")
#
#     def handsauto(self):
#         global hands_auto
#
#         if hands_auto == False:
#             time = self.time_text_field.value()
#             step = self.hansauto_button_field.value()
#
#             hands_auto = True
#
#             """time, step, roomid, teacherid, in_room_accids, callback"""
#
#             t = threading.Thread(target=hansauto,
#                                  args=(time,
#                                        step,
#                                        self.roomid,
#                                        self.teacherid,
#                                        self.in_room_accids,
#                                        self.updateHandsLabel))
#             t.start()
#
#             self.hansauto_button_field.updateButtonText("停止自动举手")
#
#         elif hands_auto == True:
#             hands_auto = False
#             self.hansauto_button_field.updateButtonText("自动举手")
#
#     def stepAddUser(self):
#         time = self.time_text_field.value()
#         step = self.step_button_field.value()
#
#         t = threading.Thread(target=stepAddUser,
#                              args=(time,
#                                    step,
#                                    self.roomid,
#                                    self.init_accids,
#                                    self.in_room_accids,
#                                    self.updateLabel,
#                                    self.setAddButtonDisabled))
#         t.start()
#
#         self.setAddButtonDisabled(True)
#
#     def lineAddUser(self):
#         time = self.time_text_field.value()
#         line = self.line_button_field.value()
#
#         t = threading.Thread(target=lineAddUser,
#                              args=(time,
#                                    line,
#                                    self.roomid,
#                                    self.init_accids,
#                                    self.in_room_accids,
#                                    self.updateLabel,
#                                    self.setAddButtonDisabled))
#         t.start()
#
#         self.setAddButtonDisabled(True)
#
#     def addUser(self):
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
#
#
#
# def auto_io(time, step, roomid, init_accids, in_room_accids, callback):
#     while io_auto:
#
#         in_room = int(step * random.random())
#         out_room = step - in_room
#
#         if in_room > len(init_accids):
#             in_room = len(init_accids)
#
#         if out_room > len(in_room_accids):
#             out_room = len(in_room_accids)
#
#         remove(out_room, roomid, init_accids, in_room_accids)
#         addUser(in_room, roomid, init_accids, in_room_accids)
#
#         callback()
#         timeing.sleep(time / 1000)
#
#
# def stepAddUser(time, step, roomid, init_accids, in_room_accids, callback, recover):
#     while init_accids:
#         addUser(step, roomid, init_accids, in_room_accids)
#         callback()
#         timeing.sleep(time / 1000)
#
#     recover(False)
#
#
# def lineAddUser(time, line, roomid, init_accids, in_room_accids, callback, recover):
#     step = 0
#     while init_accids:
#         step += line
#         addUser(step, roomid, init_accids, in_room_accids)
#         callback()
#         timeing.sleep(time / 1000)
#
#     recover(False)
#
#
# def handsup(num, in_room_accids, roomid, teacherid, func):
#     list = []
#
#     random.shuffle(in_room_accids)
#
#     for vu in in_room_accids:
#         if vu.is_handing == False:
#             list.append(vu)
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
#
#     random.shuffle(in_room_accids)
#
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
#
#
# def hansauto(time, step, roomid, teacherid, in_room_accids, callback):
#     while hands_auto:
#
#         hands_down = int(step * 0.4)
#         hands_up = step - hands_down
#
#         handsdown(hands_down, in_room_accids, roomid, teacherid, callback)
#         handsup(hands_up, in_room_accids, roomid, teacherid, callback)
#
#         timeing.sleep(time / 1000)