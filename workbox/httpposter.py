import requests
import json
import time
import random
import hashlib
import uuid
import aiohttp
from .secretUtil import _secure

"""
App Key
f0c2cb8ff29fe396e83315223ef991e2

App Secret
a3d5682e530b
"""

host = "http://dayour.mizholdings.com:8080/"
token = ""
classroomId = ""


def login(account):
    patten = "mizhu/api/mobile/login"
    url = host + patten
    play_load = {
        "account": account,
        "password": "111111",
        "phone": "",
        "verifycode": "",
        "longitude": "",
        "latitude": "",
        "loginMode": "2",
        "userId": "",
        "machine": "",
        "proType": ""
    }
    kw = {}
    _secure(play_load, kw)
    return requests.post(url=url, data=play_load, **kw)


def vote_getlist(token, classroomId):
    patten = "mizhu/api/vote/getList"
    url = host + patten
    play_load = {
        "token": token,
        "classroomId": classroomId
    }
    kw = {}
    _secure(play_load, kw)
    return requests.post(url=url, data=play_load, **kw)


def subOption(token, voteId, optionIds):
    patten = "mizhu/api/vote/subOption"
    url = host + patten
    play_load = {
        "token": token,
        "voteId": voteId,
        "optionIds": optionIds
    }
    kw = {}
    _secure(play_load, kw)
    return requests.post(url=url, data=play_load, **kw)


def getToken(account):
    json = login(account).json()

    return json["data"]["token"], json["data"]["userId"]


def classroomCodeAddUser(token, code, userId):
    patten = "mizhu/api/classInfo/classroomCodeAddUser"
    url = host + patten
    play_load = {
        "token": token,
        "classroomCode": code,
        "userId": userId
    }
    kw = {}
    _secure(play_load, kw)
    return requests.post(url=url, data=play_load, **kw)


def getCloudGroupId(code):
    """
    获取课程信息
    :param lessonId:
    :return:
        cloudGroupId， teacherCloudeAccount
    """
    token, userId = getToken("yangjiaqitest0001")
    res = classroomCodeAddUser(token, code, userId=userId)

    json = res.json()
    print(json)
    if json["result"] == 0:
        return json["data"]["classroomInfo"]["cloudGroupId"], json["data"]["classroomInfo"]["teacherCloudeAccount"]

    else:
        return 0, 0


def getVote(account, lessonId):
    token, userId = getToken(account)
    classroomId = classroomCodeAddUser(token, lessonId, userId).json()["data"]["classroomInfo"]["classroomId"]
    return vote_getlist(token, classroomId)


# 生成效验headers
def getHeaders():
    Secret = "a3d5682e530b"  # 本地秘钥
    curtime = str(int(time.time()))
    nonce = str(random.randint(1, 999999))
    AppKey = "f0c2cb8ff29fe396e83315223ef991e2"  # 云课的app key
    data = Secret + nonce + curtime
    headers = {
        "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
        "AppKey": AppKey,
        "Nonce": nonce,
        "CurTime": curtime,
        "CheckSum": hashlib.sha1(data.encode()).hexdigest()
    }

    return headers


def remove(num, roomid, init_accids, in_room_accids):
    print("remove", num)
    list = []

    if num > len(in_room_accids):
        num = len(in_room_accids)

    random.shuffle(in_room_accids)
    for i in range(num):
        list.append(in_room_accids.pop())

    init_accids.extend(list)

    remove_user(roomid, json.dumps(list, default=lambda o: str(o)))


def remove_user(roomid, json):
    url = "https://api.netease.im/nimserver/chatroom/removeRobot.action"
    play_load = {
        "roomid": roomid,
        "accids": json
    }
    print(play_load)
    res = requests.post(url=url, data=play_load, headers=getHeaders())
    print(res.text)
    return res


async def async_sendAttachMsg(data, accid, teacherid):
    """
        发送系统通知
    """
    url = "https://api.netease.im/nimserver/msg/sendAttachMsg.action"
    play_load = {
        "from": accid,  # 学生id
        "msgtype": 0,  # 点对点通知
        "to": teacherid,  # 教师id
        "attach": json.dumps(data)
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=play_load, headers=getHeaders()) as  res:
            text = await res.text()
            print(text)


def sendMsg(data, accid, roomid):
    """
    发送聊天室消息
    :param data:
    :param accid:
    :param roomid:
    :return:
    """
    url = "https://api.netease.im/nimserver/chatroom/sendMsg.action"
    play_load = {
        "roomid": roomid,
        "msgId": str(uuid.uuid4()),
        "fromAccid": accid,
        "msgType": 100,
        "attach": json.dumps(data)
    }

    return requests.post(url=url, data=play_load, headers=getHeaders())


def sendText(data, accid, roomid):
    """
    发送聊天室消息
    :param data:
    :param accid:
    :param roomid:
    :return:
    """
    url = "https://api.netease.im/nimserver/chatroom/sendMsg.action"
    play_load = {
        "roomid": roomid,
        "msgId": str(uuid.uuid4()),
        "fromAccid": accid,
        "msgType": 0,
        "attach": data
    }

    return requests.post(url=url, data=play_load, headers=getHeaders())


