#!/usr/local/bin/python3
import os
import shutil
import sys
import threading
import urllib.request
import time
import termios

import itchat
import requests

import _thread

from Robort_AutoReply import AI_Reply, TimeSayHello, myWifeReply
from Robort_Config import Robort_Conf
from Robort_Operation import fileHelp_Msg
from Snowball_CustomInfo import UserInfo
from Snowball_History import History_Dirc
from utils import KeyBoard


class Robort(threading.Thread):
    def __init__(self):
        self.robort_conf = Robort_Conf()
        threading.Thread.__init__(self)

    def run(self):
        itchat.auto_login(hotReload=True,
                          loginCallback=self.robort_conf.Log_in,
                          exitCallback=self.robort_conf.Log_out)
        city_info = urllib.request.urlopen(
            urllib.request.Request(
                'http://pv.sohu.com/cityjson')).read().decode('gb2312')
        location = city_info.split('=')[1].split(',')[2].split(':')[1].split(
            '"')[1]
        TimeNow = time.asctime(time.localtime(time.time()))
        MsgInfo = '登陆时间：' + TimeNow + '\n' + '登陆地点：' + location
        itchat.send(MsgInfo, toUserName='filehelper')
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)
        itchat.run()


# class RevokMsg:
#    def __init__(self):
#        self.msgId=[]
#        self.

if __name__ == '__main__':
    key_control = KeyBoard()
    Snowball = Robort()
    UserOwn = UserInfo(Snowball.robort_conf)
    # @itchat.msg_register(itchat.content.NOTE)
    # def replyNote(msg):
    #    print(msg)
    @itchat.msg_register(itchat.content.TEXT, isFriendChat=True)
    def Personal_Reply(msg):
        if UserOwn.Nickname == '':
            UserOwn.InfoInit(Snowball.robort_conf)
        else:
            pass
        # print(UserOwn.Wife)
        History_Dirc(UserOwn, msg)
        if msg["ToUserName"] == 'filehelper':
            # print(msg.fromUserName)
            # print(msg["ToUserName"])
            fileHelp_Msg(msg, UserOwn)
        elif msg["FromUserName"] == UserOwn.Wife[0]['UserName']:
            myWifeReply(msg, UserOwn)
        else:
            # print(msg["FromUserName"])
            # print(msg["ToUserName"])
            if UserOwn.ReplyStatu:
                SayHello = TimeSayHello(UserOwn)
                defaultReply = '我是小雪球，我的主人不在，我已经收到消息，一会儿告诉他😊'
                defaultReply = str(SayHello) + defaultReply
                if msg["FromUserName"] in UserOwn.contList:
                    AIReply = AI_Reply(UserOwn, msg)
                    return AIReply or defaultReply
                else:
                    UserOwn.contList.append(msg["FromUserName"])
                    return defaultReply
            else:
                pass

    @itchat.msg_register([itchat.content.ATTACHMENT, itchat.content.RECORDING, itchat.content.PICTURE, itchat.content.VIDEO], isFriendChat=True)
    def CollectFles(msg):
        if UserOwn.Nickname == '':
            UserOwn.InfoInit(Snowball.robort_conf)
        else:
            pass
        History_Dirc(UserOwn, msg)
        if msg["ToUserName"] == UserOwn.Username or msg[
                "ToUserName"] == 'filehelper':
            fileName = itchat.search_friends(
                userName=msg["FromUserName"])['RemarkName']
            if fileName == '':
                fileName = itchat.search_friends(
                    userName=msg["FromUserName"])['NickName']
            else:
                pass
            # print('fileName'+fileName)
            conectFile = os.path.join(UserOwn.tmpfilePath, fileName)
            try:
                if os.path.exists(conectFile) == False:
                    os.mkdir(conectFile)
                else:
                    pass
            except Exception as error:
                print('There have error!\n' + str(error))
            msg['Text'](os.path.join(conectFile, msg['FileName']))
        else:
            pass

    # @itchat.msg_register(itchat.content.TEXT,isFriendChat=True)
    # @itchat.msg_register(itchat.content.TEXT,)
    key_control.reSet()
    key_control.start()
    Snowball.start()
