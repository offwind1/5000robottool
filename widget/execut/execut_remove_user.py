from workbox.httpposter import *
# from PyQt5.QtCore import QThread
from .base_executor import BaseExecuor, BaseWorkThread


class WorkThread(BaseWorkThread):
    def func(self):
        remove(self.step,
           self.classroom.roomId,
           self.classroom.init_robot,
           self.classroom.inroom_robot)

class RemoveUser(BaseExecuor):
    name = "退出用户"
    worker_class = WorkThread