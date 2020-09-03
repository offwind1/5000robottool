from workbox.httpposter import *
from workbox.myFaker import faker
from .base_executor import BaseExecuor, BaseWorkThread


class WorkThread(BaseWorkThread):
    def func(self):
        num = self.step
        random.shuffle(self.classroom.inroom_robot)

        if num > self.classroom.get_inroom_robot_len():
            num = self.classroom.get_inroom_robot_len()

        for i in range(num):
            vuser = self.classroom.inroom_robot[i]
            vuser.sendText(faker.sentence(), self.classroom.roomId)


class SendText(BaseExecuor):
    name = "发送文本"
    worker_class = WorkThread
