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

def History_Dirc(UserOwn,msg):
        if msg["ToUserName"]!='filehelper':
            if msg["ToUserName"]==UserOwn.Username:
                fileName=itchat.search_friends(userName=msg["FromUserName"])['RemarkName']
                if fileName=='':
                    fileName=itchat.search_friends(userName=msg["FromUserName"])['NickName']
                else:
                    pass
            elif msg["FromUserName"]==UserOwn.Username:
                fileName=itchat.search_friends(userName=msg["ToUserName"])['RemarkName']
                if fileName=='':
                    fileName=itchat.search_friends(userName=msg["ToUserName"])['NickName']
                else:
                    pass
            else:
                pass
            conectFile=os.path.join(UserOwn.tmpfilePath,fileName)

            try:
                if os.path.exists(conectFile)==False:
                    os.mkdir(conectFile)
                    hisPath=os.path.join(conectFile,fileName+'.history')
                    #os.chmod(hisPath,stat.S_IRWXU)
                    hisFile=open(hisPath,"a+")
                elif os.path.exists(conectFile)==True and os.path.exists(os.path.join(conectFile,fileName+'.history'))==False:
                    hisPath=os.path.join(conectFile,fileName+'.history')
                    #os.chmod(hisPath,stat.S_IRWXU)
                    hisFile=open(hisPath,"a+")
                else:
                    hisPath=os.path.join(conectFile,fileName+'.history')
                    os.chmod(hisPath,stat.S_IRWXU)
                    hisFile=open(hisPath,"a+")
            except Exception as error:
                print('There have error!\n'+str(error))
            history=[]
            localtime = time.asctime( time.localtime(time.time()) )
            history.append(localtime+'\n')
            history.append('['+itchat.search_friends(userName=msg["FromUserName"])['NickName']+']\n')
            typeDic={3:'A picture',62:'A video',34:'A voice message',47:'An emoj',49:'A link(music or share)'}
            if msg['Type']=='Text':
                history.append(msg.text+'\n')
            elif msg['MsgType']==3 or msg['MsgType']==62 or msg['MsgType']==34 or msg['MsgType']==47 or (msg['MsgType']==49 and msg['AppMsgType']!=2001):
                history.append('['+typeDic[msg['MsgType']]+']\n')
                if msg['MsgType']==49:
                    history.append('It\'s name is :'+msg['FileName']+'\n')
                else :
                    pass
            else:
                pass
            #print(history)
            hisFile.writelines(history)
            hisFile.close()
            os.chmod(hisPath,stat.S_IRUSR)
        else:
            pass

