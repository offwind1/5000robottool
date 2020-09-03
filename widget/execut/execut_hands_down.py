# from workbox.httpposter import *
# from PyQt5.QtCore import QTimer, QThread
import asyncio
from .base_executor import BaseExecuor, BaseWorkThread
import random

class WorkThread(BaseWorkThread):
    def func(self):
        execut(self.step, self.classroom)

class HandsDown(BaseExecuor):
    name = "取消举手"
    worker_class = WorkThread

async def hansds_down_list(classroom, list, num):
    for i in range(num):
        vuser = list.pop()
        await vuser.async_userHandsdown(classroom.roomId, classroom.tercherId)


def execut(step, classroom):
    num = step
    list = []
    random.shuffle(classroom.inroom_robot)

    for vu in classroom.inroom_robot:
        if vu.is_handing == True:
            list.append(vu)

    if num > len(list):
        num = len(list)

    # asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(hansds_down_list(classroom, list, num))
