from workbox.httpposter import *
from workbox.myFaker import faker
from .base_executor import BaseExecuor, BaseWorkThread


class WorkThread(BaseWorkThread):
    def func(self):
        num = self.step
        name_list = []
        for i in range(num):
            name_list.append(faker.name())

        data = {
            "data": {
                "command": 43,
                "contents": "43:0,{};".format(",".join(name_list)),
                "room_id": self.classroom.roomId
            },
            "type": 10
        }

        sendMsg(data, self.classroom.tercherId, self.classroom.roomId)


class SendDanmu(BaseExecuor):
    name = "发送弹幕"
    worker_class = WorkThread
