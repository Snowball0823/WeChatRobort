#!/usr/local/bin/python3
import os
import sys
import stat
import time
import glob
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
import Snowball_History
from AutoReply import AI_Reply

class New_Snow(object):
    def __init__(self):
        self.tu_key=""
        self._conf=configparser.ConfigParser()
        self.path=sys.path[0]
        self._judge=os.path.exists(os.path.join(self.path,'conf.ini'))
        tmpjudge_Tmp=os.path.exists(os.path.join(self.path,'WechatFileTmp'))
        self.TmpPath=os.path.join(self.path,'WechatFileTmp')
        filejudge_Tmp=os.path.exists(os.path.join(self.path,'UploadFiles'))
        self.UploadPath=os.path.join(self.path,'UploadFiles')
        try:
            if tmpjudge_Tmp==False:
                os.mkdir(os.path.join(self.path,'WechatFileTmp'))
            else:
                pass
        except Exception as error:
            print('You have error!\n'+str(error))
        try:
            if filejudge_Tmp==False:
                os.mkdir(os.path.join(self.path,'UploadFiles'))
            else:
                pass
        except Exception as error:
            print('You have error!\n'+str(error))
        if self._judge :
            self.Get_SecKeys()
        else:
            self.Build_Conf()
    def Get_SecKeys(self):
        os.chmod(os.path.join(self.path,'conf.ini'),stat.S_IRWXU)
        #self._conf.read('conf.ini')
        self._conf.read(os.path.join(self.path,'conf.ini'))
        #self.tu_key=self.conf.get('main','key')
        conf_sec=self._conf.sections()
        #print(conf_sec)
        self._conf_True=[]
        #self._confKeys=[]
        if len(conf_sec)>1 :
            print('You have more than one section,choose a number of section')
            tmp_i=1
            for tmp in conf_sec :
                print(str(tmp_i)+'. Section='+str(conf_sec[tmp_i-1]))
                item_Tmp=self._conf.items(tmp)
                if len(item_Tmp)>0:
                    print('You have '+str(len(item_Tmp))+' keys')
                    self._conf_True.append(tmp)
                    #self._confKeys.append(item_Tmp)
                else:
                    print('You have no keys in this section!')
                tmp_i+=1
            if self._conf_True :
                while True:
                    try:
                        choise=input('Please enter the number\n')
                        choise=int(choise)
                        if choise<=0 or choise>len(conf_sec):
                            print('The choise you have entered is over the range!Please enter again!')
                            continue
                        else:
                            if conf_sec[choise-1] in self._conf_True:
                                for tmp_Key in self._conf.items(conf_sec[choise-1]):
                                    print(tmp_Key)
                                while True:
                                    try:
                                        key_Chois=input('Which key do you want to use?Please enter the number\n')
                                        key_Chois=int(key_Chois)
                                        if key_Chois<1 or key_Chois>len(self._conf.items(conf_sec[choise-1])):
                                            print('The choise you have entered is over the keys range,please enter again!')
                                            continue
                                        else:
                                            sec_Str=conf_sec[choise-1]
                                            key_Str='key'+str(key_Chois)
                                            self.tu_key=self._conf.get(sec_Str,key_Str)
                                            print('Now,you are using key=\''+str(self.tu_key)+'\'')
                                            break
                                    except Exception:
                                        print('Please enter a number!')
                            else:
                                print('The number of sections you have entered has no keys,please choise again!')
                                continue
                            break
                    except Exception:
                        print('Please enter a number!')
            else:
                print('You have no keys at all!Please add keys and new section!')
                self.Add_Conf()
        elif len(conf_sec)==1:
            print('You have only one section,we are searching your keys')
            item_Tmp=self._conf.items(conf_sec[0])
            if len(item_Tmp)>0:
                print('You have '+str(len(item_Tmp))+' keys')
                for tmp_Key in item_Tmp:
                    print(tmp_Key)
                while True:
                    try:
                        key_Chois=input('Which key do you want to use?Please enter the number\n')
                        key_Chois=int(key_Chois)
                        if key_Chois<1 or key_Chois>len(item_Tmp):
                            print('The choise you have entered is over the keys range,please enter again!')
                            continue
                        else:
                            sec_Str=conf_sec[0]
                            key_Str='key'+str(key_Chois)
                            self.tu_key=self._conf.get(sec_Str,key_Str)
                            print('Now,you are using key=\''+str(self.tu_key)+'\'')
                            break
                    except Exception:
                        print('Please enter a number!')
            else:
                print('You have no keys at all!Plaese add keys and new section!')
                self.Add_Conf()
        elif len(conf_sec)==0:
            print('Your \'conf.ini\' is empty,please add a section and a key to your \'conf.ini\'')
            self.Add_Conf()
        os.chmod(os.path.join(self.path,'conf.ini'),stat.S_IRUSR)

    def Add_Conf(self):
        self._confFile=os.open(os.path.join(self.path,'conf.ini'),os.O_RDWR|os.O_APPEND)
        sec_Num=1
        key_Numju=False
        while True:
            sec_Tmp=input('Please enter the section['+str(sec_Num)+'],enter \'enter\' to end\n')
            if len(sec_Tmp)!=0:
                str_Tmp='['+sec_Tmp+']'+'\n'
                os.write(self._confFile,str_Tmp.encode('utf-8'))
                key_Num=1
                while True:
                    key_Tmp=input('Please enter the key'+str(key_Num)+' in ['+sec_Tmp+'],enter \'enter\' to end\n')
                    if len(key_Tmp)!=0:
                        keystr_Tmp='key'+str(key_Num)+'='+key_Tmp+'\n'
                        os.write(self._confFile,keystr_Tmp.encode('utf-8'))
                        key_Num+=1
                    else:
                        break
                if key_Num>1:
                    key_Numju=True
                else:
                    pass
                sec_Num+=1
            else:
                break
        if sec_Num==1 or key_Numju==False:
            print('You have entered nothing,so we use a \'Try-Key\' to open it,if you think good,you can creat your own key in\"http://www.tuling123.com\"')
            os.write(self._confFile,'[main]\n'.encode('utf-8'))
            os.write(self._confFile,'key1=1d2678900f734aa0a23734ace8aec5b1'.encode('utf-8'))
            os.close(self._confFile)
        else:
            pass
        self.Get_SecKeys()

    def Build_Conf(self):
        print('You don\'t have a conf.ini,now we are creating!')
        while True:
            try:
                _conf_Tmp=open(os.path.join(self.path,'conf.ini'),'w+')
                _conf_Tmp.close()
                print('Creat conf.ini successful!')
                break
            except Exception as error:
                print('You have an error!\n'+str(error))
        self.Add_Conf()

    def Log_in(self):
        self.userInfo=itchat.web_init()
        print('Welcom back!'+self.userInfo['User']['NickName'])
    def Log_out(self):
        print('Bye~'+self.userInfo['User']['NickName'])


class KeyBoard (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def reSet(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        new_settings = old_settings
        #new_settings[3] = new_settings[3] & ~termios.ISIG
        new_settings[3] = new_settings[3] & ~termios.ICANON
        new_settings[3] = new_settings[3] & ~termios.ECHONL
        termios.tcsetattr(fd,termios.TCSAFLUSH,new_settings)
    def kbhit(self):
        fd = sys.stdin.fileno()
        r = select.select([sys.stdin],[],[],2)
        rcode = True
        if len(r[0]) >0:
            #rcode  = sys.stdin.read(1)
            rcode=False
        return rcode
    def run(self):
        key_Tmp=True
        while key_Tmp:
            key_Tmp=self.kbhit()
        if ~key_Tmp:
            ReplyMsg='Snowball Robort Closing now!'
            itchat.send(ReplyMsg,toUserName='filehelper')
            itchat.logout()
class Robort (threading.Thread):
    def __init__(self):
        self.robort=New_Snow()
        threading.Thread.__init__(self)
    def run(self):
        itchat.auto_login(hotReload=True,loginCallback=self.robort.Log_in,exitCallback=self.robort.Log_out)
        city_info=urllib.request.urlopen( urllib.request.Request('http://pv.sohu.com/cityjson')).read().decode('gb2312')
        location=city_info.split('=')[1].split(',')[2].split(':')[1].split('"')[1]
        TimeNow=time.asctime( time.localtime(time.time()) )
        MsgInfo='登陆时间：'+TimeNow+'\n'+'登陆地点：'+location
        itchat.send(MsgInfo,toUserName='filehelper')
        termios.tcflush(sys.stdin,termios.TCIOFLUSH)
        itchat.run()

class UserInfo :
    def __init__(self,otherInfo):
        self.turl_Key=otherInfo.tu_key
        self.Nickname=''
        self.contList=[]
        self.ClassStr=''
        self.MyStatu=[]
        self.upfileNames=[]
        self.upfilePaths=[]
        self.uploadDict={}
        self.contects=[]
        self.ReplyStatu=True
        self.WifeReSta=True
        self.managerFriend=False
        self.cmdInputJudge=False
        self.findFile=False
        self.searchFile=False
        self.uploadFile=False
        self.actCode='0'
        self.Command_Open=[u'Come on',u'启动Snowball',u'工作',u'出来']
        self.Command_Close=[u'Get out',u'Close',u'Relax',u'退下']
        self.WifeCmd_Open=[u'工作',u'回来',u'启动Snowball']
        self.WifeCmd_Close=[u'Close',u'Relax',u'退下']
        self.checkFriend=[u'整理好友列表',u'清除好友列表']
        self.UpFileCmd=[u'模糊查找',u'完整路径或文件名发送文件',u'浏览文件夹']
        self.actCodes={'1':[u'选择文件并发送',u'请输入文件序号,每个文件后加上逗号'],'2':['文件未找到,进行模糊查找',u'请输入关键字,多个文件关键字用逗号隔开'],'3':['退出文件夹操作',]}
        self.imgFile=['.png','.jpg','JPG','.jpeg','.JPEG','.bmp','.BMP','.PNG','.tiff','.raw','.RAW','.psd','.ai','.PSD','.svg','.SVG','.ico','.gif']
        self.vidFile=['.avi','.AVI','.mov','.MOV','.wmv','.WMV','.mkv','.flv','.rmvb','.FLV','.mp4','.mp3','.wav','.wma','.WMA']
        self.SayHellos=[['5','11','早上好～'],['11','13','中午好～'],['13','18','下午好～'],['18','24','晚上好～'],['0','5','夜深了，小主人都睡了，快睡吧～']]
        self.FuckSpeaking=[u'ttsb',u'sb',u'你傻逼',u'你是sb',u'傻逼吧']
        self.weekDay={u'0':u'周一',u'1':u'周二',u'2':u'周三',u'3':u'周四',u'4':u'周五',u'5':u'周六',u'6':u'周日'}
        self.SearchClass=[u'下节什么课',u'今天的课表',u'所有课表',u'明天课表',u'下节课在哪里上',u'这周第几周',u'明天有课嘛',u'今天有课嘛',u'今天下午的课',u'今天上午的课',u'明天上午的课',u'明天下午的课']
        self.ClassRelax=[u'主人,之后没有课了噢～好好休息',u'主人今天整天没有课噢～',u'',u'明天没有课噢～可以晚点起啦😊',u'主人,下节课在宿舍上噢[Smirk],没有课啦',u'',u'明天没有课噢,主人好好休息～😊',u'今天没有课噢，主人可以再睡一会儿～',u'今天下午没有课噢,可以学习一下自己的东西了',u'今天上午没有课噢～可以干自己的事情啦',u'明天上午没有课,可以睡懒觉啦～😄',u'明天下午没有课，好好学习噢～⛽️']
        self.ClassStart=['2018','2','26']
        self.ClassTable={u'周一':[[u'9',u'55',u'11',u'35',u'3教312',u'通信系统原理',u'1',u'16',u'0'],[u'13',u'30',u'19',u'40',u'知行楼606',u'电子工程设计',u'1',u'8',u'0'],[u'19',u'50',u'21',u'30',u'知行楼606',u'电子工程设计',u'1',u'6',u'0']],u'周二':[[u'9',u'55',u'11',u'35',u'3教209',u'数字语音处理与编码',u'9',u'16',u'0'],[u'13',u'30',u'16',u'40',u'科学楼809',u'通信电路与系统实验',u'2',u'14',u'2'],[u'18',u'00',u'21',u'10',u'科学楼809',u'通信电路与系统试验',u'12',u'14',u'2']],u'周三':[[u'18',u'00',u'19',u'30',u'经E201',u'就业指导课',u'1',u'8',u'1']],u'周四':[[u'8',u'00',u'9',u'30',u'3教312',u'通信系统原理',u'1',u'12',u'0'],[u'9',u'55',u'11',u'25',u'3教209',u'数字语音处理与编码',u'9',u'16',u'0'],[u'13',u'30',u'15',u'00',u'科学楼920',u'信号处理工程训练',u'2',u'13',u'0'],[u'15',u'10',u'16',u'40',u'科学楼920',u'信号处理工程训练',u'2',u'12',u'0']],u'周五':[[u'9',u'55',u'11',u'35',u'1教314',u'数字图像处理',u'1',u'16',u'0'],[u'13',u'30',u'15',u'00',u'1教214',u'信息论基础',u'1',u'16',u'0']],u'周六':[u'Relax'],u'周日':['Relax']}
    def InfoInit(self,otherClass):
        self.SearchAllClass()
        self.userInfo=otherClass.userInfo
        self.Nickname=otherClass.userInfo['User']['NickName']
        self.Username=otherClass.userInfo['User']['UserName']
        self.Wife=itchat.search_friends(name=u'宇宙世界第一无敌小可爱')
        self.tmpfilePath=otherClass.TmpPath
        self.uploadFilePath=otherClass.UploadPath
        #print('My Wife')
        #print(self.Wife[0]['Alias'])
    def SearchAllClass(self):
        self.ClassStr=''
        for key in self.ClassTable:
            self.ClassStr=self.ClassStr+key+'\n'
            if key!=u'周六' and key!=u'周日':
                for classTmp in self.ClassTable[key]:
                    self.ClassStr=self.ClassStr+classTmp[0]+':'+classTmp[1]+'~'+classTmp[2]+':'+classTmp[3]+'; '+u'教室: '+classTmp[4]+'; '+u'课程: '+classTmp[5]+'\n'
            else:
                self.ClassStr=self.ClassStr+u'休息噢～主人\n'
#class RevokMsg:
#    def __init__(self):
#        self.msgId=[]
#        self.

if __name__ == '__main__':
########################## Complete it late ##########################
    #def DeletChatRoom(chatroomName,nameList):
    def OneKeyCheckFriend():
        UserOwn.managerFriend=False
        itchat.send(u'主人,我开始搜索好友列表～',toUserName='filehelper')
        friendInfoList=itchat.get_friends(update=True)
        #for i in friendInfoList:
        #    print(i['NickName'])
        firstChatList=[]
        tmpChatList=[]
        deletChatList=[]
        tmp=[]
        j=1
        retopic='test'
        for i in range(3):
            firstChatList.append(friendInfoList[i])
        try:
            itchat.create_chatroom(firstChatList,topic=retopic+str(j))
        except Exception as error:
            print('Have an error:'+str(error))
        count=0
        chatUserName=itchat.search_chatrooms(name=retopic+str(j))
        for friendTmp in friendInfoList:
            tmp.append(friendTmp)
            if count==37:
                DeletChatRoom(retopic+str(j),tmpChatList+firstChatList)
                j+=1
                itchat.create_chatroom(firstChatList,topic=retopic+str(j))
                chatUserName=itchat.search_chatrooms(name=retopic+str(j))
                count=0
                tmpChatList.claer()
            try:
                itchat.add_member_into_chatroom(chatUserName,tmp)
            except Exception as error:
                print('You test friend error:'+str(error))
                itchat.send('主人,\"'+i['NickName']+'\"已经删除了你',toUserName='filehelper')
            count+=1
            tmpChatList.append(friendTmp)
        UserOwn.managerFriend=True
########################## Complete it late ##########################
    def FilesActInit():
        itchat.send(u'退出文件夹操作',toUserName='filehelper')
        UserOwn.actCode='0'
        UserOwn.cmdInputJudge=False
        UserOwn.findFile=False
        UserOwn.searchFile=False
        UserOwn.uploadFile=False
    def UplonadMyFiles(msg):
        if (msg.text==UserOwn.UpFileCmd[1]) and not UserOwn.uploadFile:
            pass
        elif (msg.text==UserOwn.UpFileCmd[2]) and not UserOwn.uploadFile:
            UserOwn.upfileNames.clear()
            UserOwn.upfilePaths.clear()
            UserOwn.uploadDict.clear()
            replyMsg='在上传文件夹下有这些文件:\n'
            i=0
            #改上传文件路径
            for root,dirc,files in os.walk( os.path.split(UserOwn.uploadFilePath)[0],topdown=True,followlinks=True):
                for tmp in files:
                    i+=1
                    replyMsg+=str(i)+'. '+tmp+'\n'
                    UserOwn.upfileNames.append(tmp)
                    UserOwn.upfilePaths.append(root)
            #print(UserOwn.upfileNames)
            #print(UserOwn.upfilePaths)
            try:
                UserOwn.uploadDict=dict(zip(UserOwn.upfileNames,UserOwn.upfilePaths))
            except Exception as error:
                print('You have error!\n'+str(error))
            #print(UserOwn.uploadDict)
            UserOwn.findFile=True
            UserOwn.cmdInputJudge=True
            if replyMsg=='在上传文件夹下有这些文件:\n':
                replyMsg='主人,在上传文件夹没有文件噢'
                UserOwn.cmdInputJudge=False
                itchat.send(replyMsg,toUserName='filehelper')
            else:
                itchat.send(replyMsg,toUserName='filehelper')
                keysTmp=UserOwn.actCodes.keys()
                replyMsg="可以进行以下操作:\n"
                for i in keysTmp:
                    replyMsg+=i+'. '+UserOwn.actCodes[i][0]+'\n'
                replyMsg+='请输入操作编码,如\"1\",\"2\"等'
                itchat.send(replyMsg,toUserName='filehelper')
            return
        elif UserOwn.findFile and not UserOwn.searchFile and not UserOwn.uploadFile:
            if msg.text in UserOwn.actCodes.keys():
                if msg.text=='3':
                    FilesActInit()
                    return
                else:
                    itchat.send(UserOwn.actCodes[msg.text][1],toUserName='filehelper')
                    UserOwn.actCode=msg.text
                    return
            if UserOwn.actCode!='0': 
                if UserOwn.actCode=='1':
                    UserOwn.upfilePaths.clear()
                    if ',' in msg.text:
                        fileNametmp=msg.text.split(',')
                    elif '，' in msg.text:
                        fileNametmp=msg.text.split('，')
                    for tmp in fileNametmp:
                        try:
                            tmp=int(tmp)
                            try:
                                UserOwn.upfilePaths.append(os.path.join(UserOwn.uploadDict[UserOwn.upfileNames[tmp-1]],UserOwn.upfileNames[tmp-1]))
                            except KeyError:
                                itchat.send('主人,文件: \"'+tmp+'\"不存在,将不会被发送',toUserName='filehelper')
                        except ValueError:
                            itchat.send('主人,请输入文件序号哦,\"'+tmp+'\"不是数字～',toUserName='filehelper')
                    if len(UserOwn.upfilePaths)>0:
                        UserOwn.uploadFile=True
                        itchat.send('主人,请输入需要发送的人的昵称或者你给他们的备注，多个人中间用逗号隔开噢～也可以输入\"3\"来退出',toUserName='filehelper')
                        return
                    else:
                        itchat.send('主人,没有文件将被发送,可以继续输入文件或输入\"3\"退出文件夹操作',toUserName='filehelper')
                        UserOwn.uploadFile=False
                        return
                elif UserOwn.actCode=='2':
                    if ',' in msg.text:
                        globName=msg.text.split(',')
                    elif '，' in msg.text:
                        globName=msg.text.split('，')
                    globPath=globNamesInSystem(globName)
                return
        elif UserOwn.uploadFile:
            friendError=False
            if msg.text=='3':
                FilesActInit()
                return
            else:
                if ',' in msg.text:
                    sendName=msg.text.split(',')
                elif '，' in msg.text:
                    sendName=msg.text.split('，')
                for i in sendName:
                    sendFriend=itchat.search_friends(name=i)
                    print(sendFriend)
                    if len(sendFriend)==0:
                        itchat.send('主人,你没有\"'+i+'\" 这个好友噢',toUserName='filehelper')
                        friendError=True
                    else:
                        for fileTmpPath in UserOwn.upfilePaths:
                            fileType=os.path.splitext(fileTmpPath)[1]
                            if fileType in UserOwn.imgFile:
                                uploadFileToFriend(fileTmpPath,sendFriend[0]['UserName'],isImg=True)
                            elif fileType in UserOwn.vidFile:
                                uploadFileToFriend(fileTmpPath,sendFriend[0]['UserName'],isVideo=True)
                            else:
                                uploadFileToFriend(fileTmpPath,sendFriend[0]['UserName'])
                        itchat.send('主人,好友\"'+i+'\"已经发送完毕，若有错请重新发送',toUserName='filehelper')
                itchat.send('主人,所有好友都已经发送啦,若想退出文件操作,请输入\"3\"',toUserName='filehelper')
                if friendError:
                    itchat.send('主人,刚刚有好友输入有误,可以重新输入哦,若想退出文件操作,请输入\"3\"',toUserName='filehelper')
                else:
                    UserOwn.uploadFile=False
                    UserOwn.actCode=0

    def globNamesInSystem(globNameList):
        pathDic={}
        pathTmp=[]
        
    def uploadFileToFriend(fileName,userName,isImg=False,isVideo=False):
        try:
            if isImg:
                itchat.send_image(fileName,toUserName=userName)
            elif isVideo:
                itchat.send_video(fileName,toUserName=userName)
            else:
                itchat.send_file(fileName,toUserName=userName)
            itchat.send('主人,文件:\"'+os.path.split(fileName)[1]+'\"发送成功啦～',toUserName='filehelper')
        except Exception as error:
            itchat.send('主人,出错啦!😭\n'+str(error),toUserName='filehelper')
            itchat.send('文件:'+os.path.split(fileName)[1]+'发送错误～',toUserName='filehelper')
    def TimeSayHello():
        TimeNow=time.localtime(time.time())
        #print(TimeNow)
        for timeTmp in UserOwn.SayHellos:
            if int(TimeNow[3])>=int(timeTmp[0]) and int(TimeNow[3])<int(timeTmp[1]):
                #print('hello='+timeTmp[2])
                return timeTmp[2]
            else:
                pass
    def SearchMyClass(msg):
        reply_Num=UserOwn.SearchClass.index(msg.text)
        #print('reply_Num='+str(reply_Num))
        TimeNow=time.localtime(time.time())
        hourNow=TimeNow[3]
        hourDiff=24
        weekToday=UserOwn.weekDay[str(TimeNow[6])]
        weekTomorr=UserOwn.weekDay[str(TimeNow[6]+1)]
        weekNow=datetime.date(TimeNow[0],TimeNow[1],TimeNow[2])-datetime.date(2018,2,26)
        weekNow=int(str(weekNow).split('d')[0])
        weekNow=int(weekNow/7)+1
        weekNext=datetime.date(TimeNow[0],TimeNow[1],TimeNow[2]+1)-datetime.date(2018,2,26)
        weekNext=int(str(weekNext).split('d')[0])
        weekNext=int(weekNext/7)+1
        weekDu=weekNow%2
        weekDuNext=weekNext%2
        reply_One=reply_Two=reply_Three=reply_Four=reply_Five=reply_Six=reply_Seven=reply_Eight=reply_Nine=reply_Ten=reply_Eleven=reply_Twelve=reply_Tmp_1=reply_Tmp_2=''
        reply_Three=UserOwn.ClassStr
        reply_Six='这周是第'+str(weekNow)+'周噢小主人'
        #print('reply_Three='+reply_Three)
        if reply_Num==0 or reply_Num==1 or reply_Num==4 or reply_Num==7 or reply_Num==8 or reply_Num==9:
            #print('Today='+weekToday)
            #print('')
            for classInfoTmp in UserOwn.ClassTable[weekToday]:
                try:
                    #print(classInfoTmp)
                    #print(classInfoTmp[6])
                    #+' '+str(int(classInfoTmp[8])%2)+' '+weekDu+' '+classInfoTmp[6]+' '+classInfoTmp[7])
                    if int(classInfoTmp[0])>=int(hourNow) and (int(classInfoTmp[2])-int(hourNow))<hourDiff and (classInfoTmp[8]=='0' or int(classInfoTmp[8])%2==weekDu) and (weekNow>=int(classInfoTmp[6]) and weekNow<=int(classInfoTmp[7])):
                        hourDiff=int(classInfoTmp[2])-hourNow
                        reply_One=u'下节课: \n'+classInfoTmp[0]+':'+classInfoTmp[1]+'~'+classInfoTmp[2]+':'+classInfoTmp[3]+'\n'+u'教室: '+classInfoTmp[4]+u'\n'+u'课程: '+classInfoTmp[5]+'\n'
                        delayTime=int(classInfoTmp[0])*60+int(classInfoTmp[1])-int(TimeNow[3]*60)-int(TimeNow[3])
                        #print(str(int(TimeNow[2]*60))+' '+str(TimeNow[2]))
                        #print(delayTime)
                        delayHour=int(delayTime/60)
                        delayMin=delayTime%60
                        if delayHour==0 and delayMin>=20:
                            delayTime=str(delayMin)+'分钟'
                        elif delayHour==0 and delayMin<20:
                            delayTime=str(delayMin)+'分钟,小主人要加快了噢，要迟到了～'
                        else:
                            delayTime=str(delayHour)+'小时'+str(delayMin)+'分钟'
                        #print(delayTime)
                        reply_Five=u'主人,下节课在'+classInfoTmp[4]+u'上课噢~\n'+u'下节课上课时间是: \n'+classInfoTmp[0]+':'+classInfoTmp[1]+'\n'+'距离上课还有:'+delayTime
                    else:
                        pass
                    #print(classInfoTmp[8]+' '+str(int(classInfoTmp[8])%2)+' '+weekDu+' '+classInfoTmp[6]+' '+classInfoTmp[7])
                    if (classInfoTmp[8]=='0' or int(classInfoTmp[8])%2==weekDu) and (weekNow>=int(classInfoTmp[6]) and weekNow<=int(classInfoTmp[7])):
                        reply_Two=reply_Two+classInfoTmp[0]+':'+classInfoTmp[1]+'~'+classInfoTmp[2]+':'+classInfoTmp[3]+'\n'+u'教室: '+classInfoTmp[4]+'\n'+u'课程: '+classInfoTmp[5]+'\n'
                        reply_Eight=u'小主人今天有课噢～这是今天的课表:\n'+reply_Two
                        #print('reply_Eight='+reply_Eight)
                    else:
                        pass
                    if (classInfoTmp[8]=='0' or int(classInfoTmp[8])%2==weekDu) and (int(weekNow)>=int(classInfoTmp[6]) and int(weekNow)<=int(classInfoTmp[7])) and int(classInfoTmp[0])<12:
                        reply_Tmp_1=reply_Tmp_1+classInfoTmp[0]+':'+classInfoTmp[1]+'~'+classInfoTmp[2]+':'+classInfoTmp[3]+'\n'+u'教室: '+classInfoTmp[4]+'\n'+u'课程: '+classInfoTmp[5]+'\n'
                        reply_Ten=u'主人，上午的课表是:\n'+reply_Tmp_1
                    elif (classInfoTmp[8]=='0' or int(classInfoTmp[8])%2==weekDu) and (int(weekNow)>=int(classInfoTmp[6]) and int(weekNow)<=int(classInfoTmp[7])) and (int(classInfoTmp[0])>12 and int(classInfoTmp[2])<23):
                        reply_Tmp_2=reply_Tmp_2+classInfoTmp[0]+':'+classInfoTmp[1]+'~'+classInfoTmp[2]+':'+classInfoTmp[3]+'\n'+u'教室: '+classInfoTmp[4]+'\n'+u'课程: '+classInfoTmp[5]+'\n'
                        reply_Nine=u'主人，下午的课表是:\n'+reply_Tmp_2
                    else:
                        pass
                except Exception as error:
                    print('You have today wrong!\n'+str(error))
                    if weekToday==u'周六' or weekToday==u'周日':
                        reply_One=reply_Two=reply_Five=reply_Eight=reply_Nine=reply_Ten=u'主人今天是周末哦～没有课😊'
                    else:
                        pass
        elif reply_Num==3 or reply_Num==6 or reply_Num==10 or reply_Num==11:
            for classInfoTmp in UserOwn.ClassTable[weekTomorr]:
                try:
                    if (classInfoTmp[8]=='0' or int(classInfoTmp[8])%2==weekDuNext) and (weekNext>=int(classInfoTmp[6]) and weekNext<=int(classInfoTmp[7])):
                        reply_Four=reply_Four+classInfoTmp[0]+':'+classInfoTmp[1]+'~'+classInfoTmp[2]+':'+classInfoTmp[3]+'\n'+u'教室: '+classInfoTmp[4]+'\n'+u'课程: '+classInfoTmp[5]+'\n'
                        reply_Seven=u'小主人,明天有课噢～这是明天的课表:\n'+reply_Four
                    else:
                        pass
                    if (classInfoTmp[8]=='0' or int(classInfoTmp[8])%2==weekDuNext) and (weekNow>=int(classInfoTmp[6]) and int(weekNow)<=int(classInfoTmp[7])) and int(classInfoTmp[0])<12:
                        reply_Tmp_1=reply_Tmp_1+classInfoTmp[0]+':'+classInfoTmp[1]+'~'+classInfoTmp[2]+':'+classInfoTmp[3]+'\n'+u'教室: '+classInfoTmp[4]+'\n'+u'课程: '+classInfoTmp[5]+'\n'
                        reply_Eleven=u'主人，明天上午的课表是:\n'+reply_Tmp_1
                    elif (classInfoTmp[8]=='0' or int(classInfoTmp[8])%2==weekDu) and (int(weekNow)>=int(classInfoTmp[6]) and int(weekNow)<=int(classInfoTmp[7])) and (int(classInfoTmp[0])>12 and int(classInfoTmp[2])<23):
                        reply_Tmp_2=reply_Tmp_2+classInfoTmp[0]+':'+classInfoTmp[1]+'~'+classInfoTmp[2]+':'+classInfoTmp[3]+'\n'+u'教室: '+classInfoTmp[4]+'\n'+u'课程: '+classInfoTmp[5]+'\n'
                        reply_Twelve=u'主人，明天下午的课表是:\n'+reply_Tmp_2
                    else:
                        pass
                except Exception as error:
                    print('You have tomorrow wrong!\n'+str(error))
                    if weekTomorr==u'周六' or weekTomorr==u'周日':
                        reply_Four=reply_Seven=reply_Eleven=reply_Twelve=u'主人明天是周末哦～没有课😊'
                    else:
                        pass
        else:
            pass
        reply_All=[reply_One,reply_Two,reply_Three,reply_Four,reply_Five,reply_Six,reply_Seven,reply_Eight,reply_Nine,reply_Ten,reply_Eleven,reply_Twelve]
        for i in reply_All:
            if i=='':
                numTmp=reply_All.index(i)
                reply_All[numTmp]=UserOwn.ClassRelax[numTmp]
            else:
                pass
        #print('Result='+str(reply_All[reply_Num]))
        return reply_All[reply_Num]
    def fileHelp_Msg(msg):
        if msg.text in UserOwn.Command_Open:
            if UserOwn.ReplyStatu==False:
                ReplyMsg='Now,You are opennning Snowball-Robort'
                UserOwn.ReplyStatu=True
            else:
                ReplyMsg='I\'m here!You have opened me~'
        elif msg.text in UserOwn.Command_Close:
            if UserOwn.ReplyStatu==True:
                ReplyMsg='See you later~ '+UserOwn.Nickname
                UserOwn.contList.clear()
                UserOwn.ReplyStatu=False
            else:
                ReplyMsg='I\'m only reply for you~My owener!'
        elif (msg.text not in UserOwn.SearchClass) and ('课' in  msg.text):
            msgTmp='如果想查询课表，请输入：\n'
            for cmdTmp in UserOwn.SearchClass:
                msgTmp=msgTmp+'\"'+cmdTmp+'\"'+'\n'
            ReplyMsg=msgTmp
        elif msg.text in UserOwn.SearchClass:
            ReplyTmp=SearchMyClass(msg)
            ReplyMsg=ReplyTmp
        elif (msg.text in UserOwn.UpFileCmd) or UserOwn.cmdInputJudge:
            UploadMyFiles(msg)
            return
        elif (msg.text not in UserOwn.UpFileCmd)and(('发送' in msg.text) or ('文件' in msg.text)):
            msgTmp='如果需要操作文件，请输入：\n'
            for cmdTmp in UserOwn.UpFileCmd:
                msgTmp=msgTmp+'\"'+cmdTmp+'\"'+'\n'
            ReplyMsg=msgTmp
        elif msg.text not in UserOwn.checkFriend and judgeGlob(msg):
            msgTmp='如果想清理好友列表,请输入：\n'
            for cmdTmp in UserOwn.checkFriend:
                msgTmp=msgTmp+'\"'+cmdTmp+'\"'+' 或者'
            ReplyMsg=msgTmp.rstrip(' 或者')
        elif (msg.text in UserOwn.checkFriend) and not UserOwn.managerFriend:
            msgTmp='主人,小雪球的这个功能还未完善,请耐心等候～'
            ReplyMsg=msgTmp
            #OneKeyCheckFriend()
            #return
        elif (msg.text in UserOwn.checkFriend) and UserOwn.managerFriend:
            ReplyMsg='主人,正在进行此操作,请稍等~'
        else:
            ReplyTmp=AI_Reply(UserOwn,msg)
            if ReplyTmp=='':
                ReplyMsg='I don\'t know what are speaking!'
            else:
                ReplyMsg=ReplyTmp
        itchat.send(ReplyMsg,toUserName='filehelper')
    def judgeGlob(msg):
        for tmpCheck in ['清除','管理','好友']:
            if tmpCheck in msg.text:
                tmpJudge=True
                break
            else:
                tmpJudge=False
        return tmpJudge
    def myWifeReply(msg):
        SayHello=TimeSayHello()
        wifeDefaultReply='阿妈我来啦～阿爸在忙呢，我来陪你呀😊，如果不要我陪了就输入\"Close\",\"Relax\",\"退下\" 这三个指令，我就回我的小窝啦，需要我就再输入\"回来\",\"启动Snowball\",\"工作\" 这三个指令我就会回来啦～'
        wifeDefaultReply=str(SayHello)+wifeDefaultReply
        if UserOwn.Wife[0]['UserName'] in UserOwn.contList:
            if msg.text in UserOwn.WifeCmd_Open :
                if UserOwn.WifeReSta :
                    ReplyMsg='阿妈我在呀～么么哒'
                else:
                    ReplyMsg='阿妈我来陪你啦～阿爸好想你的～❤️ '
                    UserOwn.WifeReSta=True
            elif msg.text in UserOwn.WifeCmd_Close:
                if UserOwn.WifeReSta :
                    itchat.send(u'那妈咪我先回去啦～有事叫我哦😊',toUserName=UserOwn.Wife[0]['UserName'])
                    UserOwn.WifeReSta=False
            else:
                ReplyTmp=AI_Reply(UserOwn,msg)
                if ReplyTmp=='':
                    ReplyMsg='妈咪我还小，不懂你说的，等下问阿爸吧～'
                else:
                    ReplyMsg=ReplyTmp
        else:
            UserOwn.contList.append(UserOwn.Wife[0]['UserName'])
            ReplyMsg=wifeDefaultReply
        if UserOwn.WifeReSta:
            itchat.send(ReplyMsg,toUserName=UserOwn.Wife[0]['UserName'])
    #@itchat.msg_register(itchat.content.NOTE)
    #def replyNote(msg):
    #    print(msg)
    @itchat.msg_register(itchat.content.TEXT,isFriendChat=True)
    def Personal_Reply(msg):
        if UserOwn.Nickname=='':
            UserOwn.InfoInit(Snowball.robort)
        else:
            pass
        #print(UserOwn.Wife)
        Snowball_History.History_Dirc(UserOwn,msg)
        if msg["ToUserName"]=='filehelper':
            #print(msg.fromUserName)
            #print(msg["ToUserName"])
            fileHelp_Msg(msg)
        elif msg["FromUserName"]==UserOwn.Wife[0]['UserName']:
            myWifeReply(msg)
        else:
            #print(msg["FromUserName"])
            #print(msg["ToUserName"])
            if UserOwn.ReplyStatu:
                SayHello=TimeSayHello()
                defaultReply='我是小雪球，我的主人不在，我已经收到消息，一会儿告诉他😊'
                defaultReply=str(SayHello)+defaultReply
                if msg["FromUserName"] in UserOwn.contList:
                    AIReply=AI_Reply(UserOwn,msg)
                    return AIReply or defaultReply
                else:
                    UserOwn.contList.append(msg["FromUserName"])
                    return defaultReply
            else:
                pass
    @itchat.msg_register([itchat.content.ATTACHMENT,itchat.content.RECORDING,itchat.content.PICTURE,itchat.content.VIDEO],isFriendChat=True)
    def CollectFles(msg):
        if UserOwn.Nickname=='':
            UserOwn.InfoInit(Snowball.robort)
        else:
            pass
        Snowball_History.History_Dirc(UserOwn,msg)
        if msg["ToUserName"]==UserOwn.Username or msg["ToUserName"]=='filehelper':
            fileName=itchat.search_friends(userName=msg["FromUserName"])['RemarkName']
            if fileName=='':
                fileName=itchat.search_friends(userName=msg["FromUserName"])['NickName']
            else:
                pass
            #print('fileName'+fileName)
            conectFile=os.path.join(UserOwn.tmpfilePath,fileName)
            try:
                if os.path.exists(conectFile)==False:
                    os.mkdir(conectFile)
                else:
                    pass
            except Exception as error:
                print('There have error!\n'+str(error))
            msg['Text'](os.path.join(conectFile,msg['FileName']))
        else:
            pass
    #@itchat.msg_register(itchat.content.TEXT,isFriendChat=True)
    #@itchat.msg_register(itchat.content.TEXT,)
    rob_Key=KeyBoard()
    Snowball=Robort()
    UserOwn=UserInfo(Snowball.robort)
    rob_Key.reSet()
    rob_Key.start()
    Snowball.start()

