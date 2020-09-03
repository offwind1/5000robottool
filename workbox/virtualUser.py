from .httpposter import *
import json
import db as DB
from .secretUtil import get_sign, _secure


class VirtualUser:

    def __init__(self, accid):
        self.accid = accid
        self.name = "未初始化"
        self.image = "http://images.mizholdings.com/face/default/01.gif"
        self.userId = ""
        self.is_inroom = False  # 在课堂中
        self.is_handing = False  # 在举手中

        self.vote_save = []

    def __str__(self):
        return self.accid

    def __repr__(self):
        return self.accid

    def sendText(self, data, roomid):
        res = sendText(data, self.accid, roomid)

    def me2_words(self):
        url = host + "mizhu/api/integ/words"
        play_load = {
            "token": token,
            "cloudUsrAccount": self.accid
        }
        kw = {}
        _secure(play_load, kw)
        res = requests.post(url=url, data=play_load, **kw)
        print(res.text)

    # 举手
    async def async_userHandsup(self, roomid, teacherid):
        """
        协程 举手
        :param roomid:
        :param teacherid:
        :return:
        """
        self.is_handing = True
        await self.async_hands(True, roomid, teacherid)

    async def async_userHandsdown(self, roomid, teacherid):
        """
        协程 取消举手
        :param roomid:
        :param teacherid:
        :return:
        """
        self.is_handing = False
        await self.async_hands(False, roomid, teacherid)

    async def async_hands(self, flag, roomid, teacherid):
        """
        举手IM 接口
        :param flag:
        :param roomid:
        :param teacherid:
        :return:
        """
        if flag:  # true
            contents = "1" # 举手
        else:  # false
            contents = "0" # 取消举手

        data = {
            "data": {
                "command": 40,
                "contents": contents,
                "room_id": roomid
            },
            "type": 10
        }

        await async_sendAttachMsg(data, self.accid, teacherid)

    # 添加用户
    async def async_add_user(self, roomid):
        url = "https://api.netease.im/nimserver/chatroom/addRobot.action"
        notifyExt = {
            "roomNickname": self.name,  # 要展示的昵称
            "roomAvatar": self.image,   # 要显示的头像
            "userId":self.userId,       # 用户id
            "loginMode": "3",           # 登录设备
        }

        accids = [self.accid]
        play_load = {
            "roomid": roomid,           # 聊天室id
            "accids": json.dumps(accids),   # 机器人账号列表
            "notifyExt": json.dumps(notifyExt), # 扩展字段
            "roleExt": json.dumps(notifyExt)    # 扩展字段
        }

        print(play_load)

        try:
            # 执行接口
            async with aiohttp.ClientSession() as session:
                async with session.post(url, data=play_load, headers=getHeaders()) as  res:
                    text = await res.text()
                    print(text)
        except Exception as e:
            print("网络请求失败 \n {}".format(e))

    def vote(self, optionId, voteId, room_id):
        contents = {
            "nickName": self.name,
            "optionId": optionId,
            "voteId": voteId
        }

        data = {
            "data": {
                "command": 49,
                "contents": json.dumps(contents),
                "room_id": room_id
            },
            "type": 10
        }

        subOption(self.token, voteId, optionId)
        sendMsg(data, self.accid, room_id)
        self.vote_save.append(voteId)

    @property
    def token(self):
        return DB.get_token_form_accid(self.accid)
