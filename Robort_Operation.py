import itchat
from Robort_File import UploadMyFiles
from Robort_AutoReply import AI_Reply
from Robort_Schedule import SearchMyClass

########################## Complete it late ##########################
def DeletChatRoom(chatroomName, nameList):
    pass

def OneKeyCheckFriend(UserOwn):
    UserOwn.managerFriend = False
    itchat.send(u'主人,我开始搜索好友列表～', toUserName='filehelper')
    friendInfoList = itchat.get_friends(update=True)
    # for i in friendInfoList:
    #    print(i['NickName'])
    firstChatList = []
    tmpChatList = []
    deletChatList = []
    tmp = []
    j = 1
    retopic = 'test'
    for i in range(3):
        firstChatList.append(friendInfoList[i])
    try:
        itchat.create_chatroom(firstChatList, topic=retopic + str(j))
    except Exception as error:
        print('Have an error:' + str(error))
    count = 0
    chatUserName = itchat.search_chatrooms(name=retopic + str(j))
    for friendTmp in friendInfoList:
        tmp.append(friendTmp)
        if count == 37:
            DeletChatRoom(retopic + str(j), tmpChatList + firstChatList)
            j += 1
            itchat.create_chatroom(firstChatList, topic=retopic + str(j))
            chatUserName = itchat.search_chatrooms(name=retopic + str(j))
            count = 0
            tmpChatList.claer()
        try:
            itchat.add_member_into_chatroom(chatUserName, tmp)
        except Exception as error:
            print('You test friend error:' + str(error))
            itchat.send('主人,\"' + i['NickName'] + '\"已经删除了你',
                        toUserName='filehelper')
        count += 1
        tmpChatList.append(friendTmp)
    UserOwn.managerFriend = True


def judgeGlob(msg):
    for tmpCheck in ['清除', '管理', '好友']:
        if tmpCheck in msg.text:
            tmpJudge = True
            break
        else:
            tmpJudge = False
    return tmpJudge


def fileHelp_Msg(msg, UserOwn):
    if msg.text in UserOwn.Command_Open:
        if UserOwn.ReplyStatu == False:
            ReplyMsg = 'Now,You are opennning Snowball-Robort'
            UserOwn.ReplyStatu = True
        else:
            ReplyMsg = 'I\'m here!You have opened me~'
    elif msg.text in UserOwn.Command_Close:
        if UserOwn.ReplyStatu == True:
            ReplyMsg = 'See you later~ ' + UserOwn.Nickname
            UserOwn.contList.clear()
            UserOwn.ReplyStatu = False
        else:
            ReplyMsg = 'I\'m only reply for you~My owener!'
    elif (msg.text not in UserOwn.SearchClass) and ('课' in msg.text):
        msgTmp = '如果想查询课表，请输入：\n'
        for cmdTmp in UserOwn.SearchClass:
            msgTmp = msgTmp + '\"' + cmdTmp + '\"' + '\n'
        ReplyMsg = msgTmp
    elif msg.text in UserOwn.SearchClass:
        ReplyTmp = SearchMyClass(msg, UserOwn)
        ReplyMsg = ReplyTmp
    elif (msg.text in UserOwn.UpFileCmd) or UserOwn.cmdInputJudge:
        UploadMyFiles(msg, UserOwn)
        return
    elif (msg.text not in UserOwn.UpFileCmd) and (('发送' in msg.text) or
                                                  ('文件' in msg.text)):
        msgTmp = '如果需要操作文件，请输入：\n'
        for cmdTmp in UserOwn.UpFileCmd:
            msgTmp = msgTmp + '\"' + cmdTmp + '\"' + '\n'
        ReplyMsg = msgTmp
    elif msg.text not in UserOwn.checkFriend and judgeGlob(msg):
        msgTmp = '如果想清理好友列表,请输入：\n'
        for cmdTmp in UserOwn.checkFriend:
            msgTmp = msgTmp + '\"' + cmdTmp + '\"' + ' 或者'
        ReplyMsg = msgTmp.rstrip(' 或者')
    elif (msg.text in UserOwn.checkFriend) and not UserOwn.managerFriend:
        msgTmp = '主人,小雪球的这个功能还未完善,请耐心等候～'
        ReplyMsg = msgTmp
        # OneKeyCheckFriend()
        # return
    elif (msg.text in UserOwn.checkFriend) and UserOwn.managerFriend:
        ReplyMsg = '主人,正在进行此操作,请稍等~'
    else:
        ReplyTmp = AI_Reply(UserOwn, msg)
        if ReplyTmp == '':
            ReplyMsg = 'I don\'t know what are speaking!'
        else:
            ReplyMsg = ReplyTmp
    itchat.send(ReplyMsg, toUserName='filehelper')
