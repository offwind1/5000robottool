from .base_executor import BaseExecuor, BaseWorkThread
import asyncio
import random

class WorkThread(BaseWorkThread):
    def func(self):
        execut(self.step, self.classroom)


class HandsUp(BaseExecuor):
    name = "用户举手"
    worker_class = WorkThread

async def hans_up_list(classroom, list, num):
    for i in range(num):
        vuser = list.pop()
        await vuser.async_userHandsup(classroom.roomId, classroom.tercherId)


def execut(step, classroom):
    num = step
    list = []
    random.shuffle(classroom.inroom_robot)

    for vu in classroom.inroom_robot:
        if vu.is_handing == False:
            list.append(vu)

    if num > len(list):
        num = len(list)

    # asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(hans_up_list(classroom, list, num))
