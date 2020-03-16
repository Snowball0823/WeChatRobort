#!/usr/local/bin/python3
import configparser
import datetime
import os
import select
import shutil
import stat
import sys
import termios
import threading
import time
import urllib.request

import itchat
import requests

import _thread


def AI_Reply(UserOwn, msg):
    apiUrl = 'http://openapi.tuling123.com/openapi/api'
    # turKey=Snowball.robort.tu_key
    turKey = UserOwn.turl_Key
    data_Body = {'key': turKey, 'info': msg.text.encode(
        'utf8'), 'userid': 'Snowball'}
    # msg.text.encode('utf8')
    # print('info'+str(data_Body['info']))
    try:
        req = requests.post(apiUrl, data=data_Body).json()
        # print('req{0}'.format(req))
        if req['code'] == 100000:
            result = req['text']
        elif req['code'] == 200000:
            result = str(req['text'])+'\n'+'链接:'+str(req['url'])
        elif req['code'] == 302000:
            result = str(req['text'])+'\n'
            for Tmp in req['list']:
                artical = '【'+Tmp['source']+'】:' + \
                    Tmp['article']+'\n'+'链接:'+Tmp['detailurl']
                result += artical+'\n'
        elif req['code'] == 308000:
            result = str(req['text'])+'\n'
            for Tmp in req['list']:
                artical = '【'+Tmp['name']+'】:'+'\n'+'配料：' + \
                    Tmp['info']+'\n'+'链接:'+Tmp['detailurl']
                result += artical+'\n'
        else:
            result = str(req)
        return result
    except:
        return ''
    #print('Your turKey='+turKey)


def TimeSayHello(UserOwn):
    TimeNow = time.localtime(time.time())
    # print(TimeNow)
    for timeTmp in UserOwn.SayHellos:
        if int(TimeNow[3]) >= int(timeTmp[0]) and int(TimeNow[3]) < int(
                timeTmp[1]):
            # print('hello='+timeTmp[2])
            return timeTmp[2]
        else:
            pass


def myWifeReply(msg, UserOwn):
    SayHello = TimeSayHello(UserOwn)
    wifeDefaultReply = '阿妈我来啦～阿爸在忙呢，我来陪你呀😊，如果不要我陪了就输入\"Close\",\"Relax\",\"退下\" 这三个指令，我就回我的小窝啦，需要我就再输入\"回来\",\"启动Snowball\",\"工作\" 这三个指令我就会回来啦～'
    wifeDefaultReply = str(SayHello) + wifeDefaultReply
    if UserOwn.Wife[0]['UserName'] in UserOwn.contList:
        if msg.text in UserOwn.WifeCmd_Open:
            if UserOwn.WifeReSta:
                ReplyMsg = '阿妈我在呀～么么哒'
            else:
                ReplyMsg = '阿妈我来陪你啦～阿爸好想你的～❤️ '
                UserOwn.WifeReSta = True
        elif msg.text in UserOwn.WifeCmd_Close:
            if UserOwn.WifeReSta:
                itchat.send(u'那妈咪我先回去啦～有事叫我哦😊',
                            toUserName=UserOwn.Wife[0]['UserName'])
                UserOwn.WifeReSta = False
        else:
            ReplyTmp = AI_Reply(UserOwn, msg)
            if ReplyTmp == '':
                ReplyMsg = '妈咪我还小，不懂你说的，等下问阿爸吧～'
            else:
                ReplyMsg = ReplyTmp
    else:
        UserOwn.contList.append(UserOwn.Wife[0]['UserName'])
        ReplyMsg = wifeDefaultReply
    if UserOwn.WifeReSta:
        itchat.send(ReplyMsg, toUserName=UserOwn.Wife[0]['UserName'])
