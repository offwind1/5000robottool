from workbox.httpposter import *
from workbox.virtualUser import VirtualUser


class Singleton():

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "onlyone"):
            cls.onlyone = super().__new__(cls)
        return cls.onlyone


class ClassRoom():
    onlyone = None

    @classmethod
    def singleton(cls):
        if cls.onlyone is None:
            cls.onlyone = ClassRoom()
        return cls.onlyone

    def __init__(self):
        super().__init__()

        self.init_robot = []
        self.inroom_robot = []
        self.max_len = 0

        self.roomId = None
        self.tercherId = None

        self.code = ""

    def invest(self):
        if self.roomId:
            return True
        return False

    def init(self, code):
        self.code = code

        self.init_robot.clear()
        self.inroom_robot.clear()
        self.roomId, self.tercherId = getCloudGroupId(code)
        loadAccids(self.init_robot)
        self.max_len = self.get_init_robot_len()

    def get_init_robot_len(self):
        return len(self.init_robot)

    def get_inroom_robot_len(self):
        return len(self.inroom_robot)

    def get_hands_info(self):
        is_handing = 0
        no_handing = 0

        for vu in self.inroom_robot:
            if vu.is_handing == False:
                no_handing += 1
            elif vu.is_handing == True:
                is_handing += 1

        return is_handing, no_handing

    def getVoteInfo(self):
        return getVote("yangjiaqitest0001", self.code)

    def showSelf(self):
        print(self.init_robot)
        print(self.inroom_robot)
        print(self.roomId)
        print(self.tercherId)


def loadAccids(accids: list):
    loadAccidsForFilename(accids, "robot5000")

def loadAccidsForFilename(accids: list, file_name):
    with open(file_name, "r") as f:
        for line in f.readlines():
            line = line.strip()
            accid, robot_name, photo_id, userId = line.split(",")
            vuser = VirtualUser(accid)
            vuser.name = robot_name
            vuser.image = photo_id
            vuser.userId = userId
            accids.append(vuser)

    random.shuffle(accids)
