#!/usr/local/bin/python3
import os
import sys
import stat
import time
import shutil
import select
import itchat
import termios
import _thread
import datetime
import requests
import threading
import configparser
import urllib.request

def AI_Reply(UserOwn,msg):
    apiUrl = 'http://openapi.tuling123.com/openapi/api'
    #turKey=Snowball.robort.tu_key
    turKey=UserOwn.turl_Key
    data_Body={'key':turKey,'info':msg.text.encode('utf8'),'userid':'Snowball'}
    #msg.text.encode('utf8')
    #print('info'+str(data_Body['info']))
    try:
        req = requests.post(apiUrl, data=data_Body).json()
        #print('req{0}'.format(req))
        if req['code']==100000:
            result=req['text']
        elif req['code']==200000:
            result=str(req['text'])+'\n'+'链接:'+str(req['url'])
        elif req['code']==302000:
            result=str(req['text'])+'\n'
            for Tmp in req['list']:
                artical='【'+Tmp['source']+'】:'+Tmp['article']+'\n'+'链接:'+Tmp['detailurl']
                result+=artical+'\n'
        elif req['code']==308000:
            result=str(req['text'])+'\n'
            for Tmp in req['list']:
                artical='【'+Tmp['name']+'】:'+'\n'+'配料：'+Tmp['info']+'\n'+'链接:'+Tmp['detailurl']
                result+=artical+'\n'
        else:
            result=str(req)
        return result
    except:
        return ''
    #print('Your turKey='+turKey)

