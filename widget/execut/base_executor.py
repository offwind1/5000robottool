
from PyQt5.QtCore import QThread
import time
import asyncio

class BaseWorkThread(QThread):

    def __init__(self, executor, time, step, classroom):
        super().__init__()
        self.executor = executor
        self.time = time
        self.step = step
        self.classroom = classroom

    def run(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        while self.executor.flag:
            self.func()
            time.sleep(self.time / 1000)

    def func(self):
        pass

class BaseExecuor(object):
    worker_class = None
    name = ""

    def __init__(self):
        self.flag = False
        self.worker = None

    def start(self, *args):
        print(args)
        self.flag = True

        self.worker = self.worker_class(self, *args)
        self.worker.start()

    def stop(self):
        self.flag = False
