########################## Complete it late ##########################
def FilesActInit(UserOwn):
    itchat.send(u'退出文件夹操作', toUserName='filehelper')
    UserOwn.actCode = '0'
    UserOwn.cmdInputJudge = False
    UserOwn.findFile = False
    UserOwn.searchFile = False
    UserOwn.uploadFile = False


def globNamesInSystem(globNameList):
    pathDic = {}
    pathTmp = []


def uploadFileToFriend(fileName, userName, isImg=False, isVideo=False):
    try:
        if isImg:
            itchat.send_image(fileName, toUserName=userName)
        elif isVideo:
            itchat.send_video(fileName, toUserName=userName)
        else:
            itchat.send_file(fileName, toUserName=userName)
        itchat.send('主人,文件:\"' + os.path.split(fileName)[1] + '\"发送成功啦～',
                    toUserName='filehelper')
    except Exception as error:
        itchat.send('主人,出错啦!😭\n' + str(error), toUserName='filehelper')
        itchat.send('文件:' + os.path.split(fileName)[1] + '发送错误～',
                    toUserName='filehelper')

def UploadMyFiles(msg, UserOwn):
    if (msg.text == UserOwn.UpFileCmd[1]) and not UserOwn.uploadFile:
        pass
    elif (msg.text == UserOwn.UpFileCmd[2]) and not UserOwn.uploadFile:
        UserOwn.upfileNames.clear()
        UserOwn.upfilePaths.clear()
        UserOwn.uploadDict.clear()
        replyMsg = '在上传文件夹下有这些文件:\n'
        i = 0
        # 改上传文件路径
        for root, dirc, files in os.walk(os.path.split(
            UserOwn.uploadFilePath)[0],
                topdown=True,
                followlinks=True):
            for tmp in files:
                i += 1
                replyMsg += str(i) + '. ' + tmp + '\n'
                UserOwn.upfileNames.append(tmp)
                UserOwn.upfilePaths.append(root)
        # print(UserOwn.upfileNames)
        # print(UserOwn.upfilePaths)
        try:
            UserOwn.uploadDict = dict(
                zip(UserOwn.upfileNames, UserOwn.upfilePaths))
        except Exception as error:
            print('You have error!\n' + str(error))
        # print(UserOwn.uploadDict)
        UserOwn.findFile = True
        UserOwn.cmdInputJudge = True
        if replyMsg == '在上传文件夹下有这些文件:\n':
            replyMsg = '主人,在上传文件夹没有文件噢'
            UserOwn.cmdInputJudge = False
            itchat.send(replyMsg, toUserName='filehelper')
        else:
            itchat.send(replyMsg, toUserName='filehelper')
            keysTmp = UserOwn.actCodes.keys()
            replyMsg = "可以进行以下操作:\n"
            for i in keysTmp:
                replyMsg += i + '. ' + UserOwn.actCodes[i][0] + '\n'
            replyMsg += '请输入操作编码,如\"1\",\"2\"等'
            itchat.send(replyMsg, toUserName='filehelper')
        return
    elif UserOwn.findFile and not UserOwn.searchFile and not UserOwn.uploadFile:
        if msg.text in UserOwn.actCodes.keys():
            if msg.text == '3':
                FilesActInit(UserOwn)
                return
            else:
                itchat.send(UserOwn.actCodes[msg.text][1],
                            toUserName='filehelper')
                UserOwn.actCode = msg.text
                return
        if UserOwn.actCode != '0':
            if UserOwn.actCode == '1':
                UserOwn.upfilePaths.clear()
                if ',' in msg.text:
                    fileNametmp = msg.text.split(',')
                elif '，' in msg.text:
                    fileNametmp = msg.text.split('，')
                for tmp in fileNametmp:
                    try:
                        tmp = int(tmp)
                        try:
                            UserOwn.upfilePaths.append(
                                os.path.join(
                                    UserOwn.uploadDict[UserOwn.upfileNames[
                                        tmp - 1]],
                                    UserOwn.upfileNames[tmp - 1]))
                        except KeyError:
                            itchat.send('主人,文件: \"' + tmp + '\"不存在,将不会被发送',
                                        toUserName='filehelper')
                    except ValueError:
                        itchat.send('主人,请输入文件序号哦,\"' + tmp + '\"不是数字～',
                                    toUserName='filehelper')
                if len(UserOwn.upfilePaths) > 0:
                    UserOwn.uploadFile = True
                    itchat.send(
                        '主人,请输入需要发送的人的昵称或者你给他们的备注，多个人中间用逗号隔开噢～也可以输入\"3\"来退出',
                        toUserName='filehelper')
                    return
                else:
                    itchat.send('主人,没有文件将被发送,可以继续输入文件或输入\"3\"退出文件夹操作',
                                toUserName='filehelper')
                    UserOwn.uploadFile = False
                    return
            elif UserOwn.actCode == '2':
                if ',' in msg.text:
                    globName = msg.text.split(',')
                elif '，' in msg.text:
                    globName = msg.text.split('，')
                globPath = globNamesInSystem(globName)
            return
    elif UserOwn.uploadFile:
        friendError = False
        if msg.text == '3':
            FilesActInit(UserOwn)
            return
        else:
            if ',' in msg.text:
                sendName = msg.text.split(',')
            elif '，' in msg.text:
                sendName = msg.text.split('，')
            for i in sendName:
                sendFriend = itchat.search_friends(name=i)
                print(sendFriend)
                if len(sendFriend) == 0:
                    itchat.send('主人,你没有\"' + i + '\" 这个好友噢',
                                toUserName='filehelper')
                    friendError = True
                else:
                    for fileTmpPath in UserOwn.upfilePaths:
                        fileType = os.path.splitext(fileTmpPath)[1]
                        if fileType in UserOwn.imgFile:
                            uploadFileToFriend(fileTmpPath,
                                               sendFriend[0]['UserName'],
                                               isImg=True)
                        elif fileType in UserOwn.vidFile:
                            uploadFileToFriend(fileTmpPath,
                                               sendFriend[0]['UserName'],
                                               isVideo=True)
                        else:
                            uploadFileToFriend(fileTmpPath,
                                               sendFriend[0]['UserName'])
                    itchat.send('主人,好友\"' + i + '\"已经发送完毕，若有错请重新发送',
                                toUserName='filehelper')
            itchat.send('主人,所有好友都已经发送啦,若想退出文件操作,请输入\"3\"',
                        toUserName='filehelper')
            if friendError:
                itchat.send('主人,刚刚有好友输入有误,可以重新输入哦,若想退出文件操作,请输入\"3\"',
                            toUserName='filehelper')
            else:
                UserOwn.uploadFile = False
                UserOwn.actCode = 0
