from workbox.httpposter import *
from .base_executor import BaseExecuor, BaseWorkThread
import asyncio


class WorkThread(BaseWorkThread):

    def func(self):
        async_addUser(self.step, self.classroom)


class AddUser(BaseExecuor):
    name = "加入用户"
    worker_class = WorkThread


async def async_add_list(roomid, list):
    for vuser in list:
        await vuser.async_add_user(roomid)


def async_addUser(num, classroom):
    list = []
    if num > len(classroom.init_robot):
        num = len(classroom.init_robot)

    print("add ", num)

    for i in range(num):
        list.append(classroom.init_robot.pop())
    classroom.inroom_robot.extend(list)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_add_list(classroom.roomId, list))
