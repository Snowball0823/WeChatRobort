class UserInfo:
    def __init__(self, otherInfo):
        self.turl_Key = otherInfo.tu_key
        self.Nickname = ''
        self.contList = []
        self.ClassStr = ''
        self.MyStatu = []
        self.upfileNames = []
        self.upfilePaths = []
        self.uploadDict = {}
        self.contects = []
        self.ReplyStatu = True
        self.WifeReSta = True
        self.managerFriend = False
        self.cmdInputJudge = False
        self.findFile = False
        self.searchFile = False
        self.uploadFile = False
        self.actCode = '0'
        self.Command_Open = [u'Come on', u'启动Snowball', u'工作', u'出来']
        self.Command_Close = [u'Get out', u'Close', u'Relax', u'退下']
        self.WifeCmd_Open = [u'工作', u'回来', u'启动Snowball']
        self.WifeCmd_Close = [u'Close', u'Relax', u'退下']
        self.checkFriend = [u'整理好友列表', u'清除好友列表']
        self.UpFileCmd = [u'模糊查找', u'完整路径或文件名发送文件', u'浏览文件夹']
        self.actCodes = {
            '1': [u'选择文件并发送', u'请输入文件序号,每个文件后加上逗号'],
            '2': ['文件未找到,进行模糊查找', u'请输入关键字,多个文件关键字用逗号隔开'],
            '3': [
                '退出文件夹操作',
            ]
        }
        self.imgFile = [
            '.png', '.jpg', 'JPG', '.jpeg', '.JPEG', '.bmp', '.BMP', '.PNG',
            '.tiff', '.raw', '.RAW', '.psd', '.ai', '.PSD', '.svg', '.SVG',
            '.ico', '.gif'
        ]
        self.vidFile = [
            '.avi', '.AVI', '.mov', '.MOV', '.wmv', '.WMV', '.mkv', '.flv',
            '.rmvb', '.FLV', '.mp4', '.mp3', '.wav', '.wma', '.WMA'
        ]
        self.SayHellos = [['5', '11', '早上好～'], ['11', '13', '中午好～'],
                          ['13', '18', '下午好～'], ['18', '24', '晚上好～'],
                          ['0', '5', '夜深了，小主人都睡了，快睡吧～']]
        self.FuckSpeaking = [u'ttsb', u'sb', u'你傻逼', u'你是sb', u'傻逼吧']
        self.weekDay = {
            u'0': u'周一',
            u'1': u'周二',
            u'2': u'周三',
            u'3': u'周四',
            u'4': u'周五',
            u'5': u'周六',
            u'6': u'周日'
        }
        self.SearchClass = [
            u'下节什么课', u'今天的课表', u'所有课表', u'明天课表', u'下节课在哪里上', u'这周第几周',
            u'明天有课嘛', u'今天有课嘛', u'今天下午的课', u'今天上午的课', u'明天上午的课', u'明天下午的课'
        ]
        self.ClassRelax = [
            u'主人,之后没有课了噢～好好休息', u'主人今天整天没有课噢～', u'', u'明天没有课噢～可以晚点起啦😊',
            u'主人,下节课在宿舍上噢[Smirk],没有课啦', u'', u'明天没有课噢,主人好好休息～😊',
            u'今天没有课噢，主人可以再睡一会儿～', u'今天下午没有课噢,可以学习一下自己的东西了',
            u'今天上午没有课噢～可以干自己的事情啦', u'明天上午没有课,可以睡懒觉啦～😄', u'明天下午没有课，好好学习噢～⛽️'
        ]
        self.ClassStart = ['2018', '2', '26']
        self.ClassTable = {
            u'周一': [[
                u'9', u'55', u'11', u'35', u'3教312', u'通信系统原理', u'1', u'16',
                u'0'
            ],
                    [
                        u'13', u'30', u'19', u'40', u'知行楼606', u'电子工程设计', u'1',
                        u'8', u'0'
                    ],
                    [
                        u'19', u'50', u'21', u'30', u'知行楼606', u'电子工程设计', u'1',
                        u'6', u'0'
                    ]],
            u'周二': [[
                u'9', u'55', u'11', u'35', u'3教209', u'数字语音处理与编码', u'9', u'16',
                u'0'
            ],
                    [
                        u'13', u'30', u'16', u'40', u'科学楼809', u'通信电路与系统实验',
                        u'2', u'14', u'2'
                    ],
                    [
                        u'18', u'00', u'21', u'10', u'科学楼809', u'通信电路与系统试验',
                        u'12', u'14', u'2'
                    ]],
            u'周三': [[
                u'18', u'00', u'19', u'30', u'经E201', u'就业指导课', u'1', u'8',
                u'1'
            ]],
            u'周四': [[
                u'8', u'00', u'9', u'30', u'3教312', u'通信系统原理', u'1', u'12',
                u'0'
            ],
                    [
                        u'9', u'55', u'11', u'25', u'3教209', u'数字语音处理与编码',
                        u'9', u'16', u'0'
                    ],
                    [
                        u'13', u'30', u'15', u'00', u'科学楼920', u'信号处理工程训练',
                        u'2', u'13', u'0'
                    ],
                    [
                        u'15', u'10', u'16', u'40', u'科学楼920', u'信号处理工程训练',
                        u'2', u'12', u'0'
                    ]],
            u'周五': [[
                u'9', u'55', u'11', u'35', u'1教314', u'数字图像处理', u'1', u'16',
                u'0'
            ],
                    [
                        u'13', u'30', u'15', u'00', u'1教214', u'信息论基础', u'1',
                        u'16', u'0'
                    ]],
            u'周六': [u'Relax'],
            u'周日': ['Relax']
        }

    def InfoInit(self, otherClass):
        self.SearchAllClass()
        self.userInfo = otherClass.userInfo
        self.Nickname = otherClass.userInfo['User']['NickName']
        self.Username = otherClass.userInfo['User']['UserName']
        self.Wife = itchat.search_friends(name=u'宇宙世界第一无敌小可爱')
        self.tmpfilePath = otherClass.TmpPath
        self.uploadFilePath = otherClass.UploadPath
        #print('My Wife')
        #print(self.Wife[0]['Alias'])
    def SearchAllClass(self):
        self.ClassStr = ''
        for key in self.ClassTable:
            self.ClassStr = self.ClassStr + key + '\n'
            if key != u'周六' and key != u'周日':
                for classTmp in self.ClassTable[key]:
                    self.ClassStr = self.ClassStr + classTmp[
                        0] + ':' + classTmp[1] + '~' + classTmp[
                            2] + ':' + classTmp[3] + '; ' + u'教室: ' + classTmp[
                                4] + '; ' + u'课程: ' + classTmp[5] + '\n'
            else:
                self.ClassStr = self.ClassStr + u'休息噢～主人\n'