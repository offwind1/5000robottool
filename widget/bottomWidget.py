from model.window import *
from model.model import *
from widget.executeWidget import ExecuteWidget
from classRoom import ClassRoom
from PyQt5.QtGui import *


class InOutWidget(BaseWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setWidget(self):
        self.add_button = QPushButton("+")
        self.add_button.clicked.connect(self.add_view)
        self.addWidget(self.add_button)

    def add_view(self):
        self.from_layout.addRow(ExecuteWidget())


class VoteWidget(BaseWidget):
    def __init__(self):
        super().__init__()
        self.classRoom = ClassRoom.singleton()

    def setWidget(self):
        self.start_button = QPushButton("获取投票信息")
        self.start_button.clicked.connect(self.get_vote_info)
        self.addWidget(self.start_button)

        self.vote_combo = QComboBox()
        self.vote_combo.currentIndexChanged.connect(self.changeView)
        self.addWidget(self.vote_combo)

        self.main_view = QStackedWidget()
        self.addWidget(self.main_view)

    def get_vote_info(self):
        if not self.classRoom.invest():
            QMessageBox.about(self, "提示", "未初始化课程")
            return

        self.vote_combo.clear()
        self.clear_Stacked()

        for vote in self.classRoom.getVoteInfo().json()["data"]["voteList"]:
            self.addMiddleWidget(vote.get("voteContent", "无"), SubVoteWidget(vote))

    def addMiddleWidget(self, tag, view):
        self.vote_combo.addItem(tag, view)
        self.main_view.addWidget(view)

    def changeView(self, index):
        self.main_view.setCurrentIndex(index)

    def clear_Stacked(self):
        while self.main_view.count() > 0:
            view = self.main_view.widget(0)
            self.main_view.removeWidget(view)


class SubVoteWidget(BaseWidget):

    def __init__(self, vote):
        super().__init__()

        self.classRoom = ClassRoom.singleton()
        for voteOption in vote["voteOptionList"]:
            setattr(self, voteOption["optionName"], ButtonSpinBoxField(self, voteOption["optionName"],
                                                                       lambda v, x=voteOption: self.vote(x)))

    def vote(self, voteOption):
        optionName = voteOption["optionName"]
        voteId = voteOption["voteId"]
        optionId = voteOption["optionId"]

        value = getattr(self, optionName).value()

        index = 0
        for robot in self.classRoom.inroom_robot:
            if voteId not in robot.vote_save:
                robot.vote(optionId, voteId, self.classRoom.roomId)
                index += 1
            if index >= value:
                break

        print(voteOption)


class BottomWidget(QTabWidget):

    def __init__(self):
        super().__init__()

        self.addTab(InOutWidget(), "用户进出")
        # self.addTab(VoteWidget(), "投票")
