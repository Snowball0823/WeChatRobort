import os,sys
import configparser
import itchat
import stat

class Robort_Conf(object):
    def __init__(self):
        self.tu_key = ""
        self._conf = configparser.ConfigParser()
        self.path = sys.path[0]
        self._judge = os.path.exists(os.path.join(self.path, 'conf.ini'))
        tmpjudge_Tmp = os.path.exists(os.path.join(self.path, 'WechatFileTmp'))
        self.TmpPath = os.path.join(self.path, 'WechatFileTmp')
        filejudge_Tmp = os.path.exists(os.path.join(self.path, 'UploadFiles'))
        self.UploadPath = os.path.join(self.path, 'UploadFiles')
        try:
            if tmpjudge_Tmp == False:
                os.mkdir(os.path.join(self.path, 'WechatFileTmp'))
            else:
                pass
        except Exception as error:
            print('You have error!\n' + str(error))
        try:
            if filejudge_Tmp == False:
                os.mkdir(os.path.join(self.path, 'UploadFiles'))
            else:
                pass
        except Exception as error:
            print('You have error!\n' + str(error))
        if self._judge:
            self.Get_SecKeys()
        else:
            self.Build_Conf()

    def Get_SecKeys(self):
        os.chmod(os.path.join(self.path, 'conf.ini'), stat.S_IRWXU)
        #self._conf.read('conf.ini')
        self._conf.read(os.path.join(self.path, 'conf.ini'))
        #self.tu_key=self.conf.get('main','key')
        conf_sec = self._conf.sections()
        #print(conf_sec)
        self._conf_True = []
        #self._confKeys=[]
        if len(conf_sec) > 1:
            print('You have more than one section,choose a number of section')
            tmp_i = 1
            for tmp in conf_sec:
                print(str(tmp_i) + '. Section=' + str(conf_sec[tmp_i - 1]))
                item_Tmp = self._conf.items(tmp)
                if len(item_Tmp) > 0:
                    print('You have ' + str(len(item_Tmp)) + ' keys')
                    self._conf_True.append(tmp)
                    #self._confKeys.append(item_Tmp)
                else:
                    print('You have no keys in this section!')
                tmp_i += 1
            if self._conf_True:
                while True:
                    try:
                        choise = input('Please enter the number\n')
                        choise = int(choise)
                        if choise <= 0 or choise > len(conf_sec):
                            print(
                                'The choise you have entered is over the range!Please enter again!'
                            )
                            continue
                        else:
                            if conf_sec[choise - 1] in self._conf_True:
                                for tmp_Key in self._conf.items(
                                        conf_sec[choise - 1]):
                                    print(tmp_Key)
                                while True:
                                    try:
                                        key_Chois = input(
                                            'Which key do you want to use?Please enter the number\n'
                                        )
                                        key_Chois = int(key_Chois)
                                        if key_Chois < 1 or key_Chois > len(
                                                self._conf.items(
                                                    conf_sec[choise - 1])):
                                            print(
                                                'The choise you have entered is over the keys range,please enter again!'
                                            )
                                            continue
                                        else:
                                            sec_Str = conf_sec[choise - 1]
                                            key_Str = 'key' + str(key_Chois)
                                            self.tu_key = self._conf.get(
                                                sec_Str, key_Str)
                                            print('Now,you are using key=\'' +
                                                  str(self.tu_key) + '\'')
                                            break
                                    except Exception:
                                        print('Please enter a number!')
                            else:
                                print(
                                    'The number of sections you have entered has no keys,please choise again!'
                                )
                                continue
                            break
                    except Exception:
                        print('Please enter a number!')
            else:
                print(
                    'You have no keys at all!Please add keys and new section!')
                self.Add_Conf()
        elif len(conf_sec) == 1:
            print('You have only one section,we are searching your keys')
            item_Tmp = self._conf.items(conf_sec[0])
            if len(item_Tmp) > 0:
                print('You have ' + str(len(item_Tmp)) + ' keys')
                for tmp_Key in item_Tmp:
                    print(tmp_Key)
                while True:
                    try:
                        key_Chois = input(
                            'Which key do you want to use?Please enter the number\n'
                        )
                        key_Chois = int(key_Chois)
                        if key_Chois < 1 or key_Chois > len(item_Tmp):
                            print(
                                'The choise you have entered is over the keys range,please enter again!'
                            )
                            continue
                        else:
                            sec_Str = conf_sec[0]
                            key_Str = 'key' + str(key_Chois)
                            self.tu_key = self._conf.get(sec_Str, key_Str)
                            print('Now,you are using key=\'' +
                                  str(self.tu_key) + '\'')
                            break
                    except Exception:
                        print('Please enter a number!')
            else:
                print(
                    'You have no keys at all!Plaese add keys and new section!')
                self.Add_Conf()
        elif len(conf_sec) == 0:
            print(
                'Your \'conf.ini\' is empty,please add a section and a key to your \'conf.ini\''
            )
            self.Add_Conf()
        os.chmod(os.path.join(self.path, 'conf.ini'), stat.S_IRUSR)

    def Add_Conf(self):
        self._confFile = os.open(os.path.join(self.path, 'conf.ini'),
                                 os.O_RDWR | os.O_APPEND)
        sec_Num = 1
        key_Numju = False
        while True:
            sec_Tmp = input('Please enter the section[' + str(sec_Num) +
                            '],enter \'enter\' to end\n')
            if len(sec_Tmp) != 0:
                str_Tmp = '[' + sec_Tmp + ']' + '\n'
                os.write(self._confFile, str_Tmp.encode('utf-8'))
                key_Num = 1
                while True:
                    key_Tmp = input('Please enter the key' + str(key_Num) +
                                    ' in [' + sec_Tmp +
                                    '],enter \'enter\' to end\n')
                    if len(key_Tmp) != 0:
                        keystr_Tmp = 'key' + str(
                            key_Num) + '=' + key_Tmp + '\n'
                        os.write(self._confFile, keystr_Tmp.encode('utf-8'))
                        key_Num += 1
                    else:
                        break
                if key_Num > 1:
                    key_Numju = True
                else:
                    pass
                sec_Num += 1
            else:
                break
        if sec_Num == 1 or key_Numju == False:
            print(
                'You have entered nothing,so we use a \'Try-Key\' to open it,if you think good,you can creat your own key in\"http://www.tuling123.com\"'
            )
            os.write(self._confFile, '[main]\n'.encode('utf-8'))
            os.write(self._confFile,
                     'key1=1d2678900f734aa0a23734ace8aec5b1'.encode('utf-8'))
            os.close(self._confFile)
        else:
            pass
        self.Get_SecKeys()

    def Build_Conf(self):
        print('You don\'t have a conf.ini,now we are creating!')
        while True:
            try:
                _conf_Tmp = open(os.path.join(self.path, 'conf.ini'), 'w+')
                _conf_Tmp.close()
                print('Creat conf.ini successful!')
                break
            except Exception as error:
                print('You have an error!\n' + str(error))
        self.Add_Conf()
    
    def Log_in(self):
        self.userInfo = itchat.web_init()
        print('Welcom back!' + self.userInfo['User']['NickName'])

    def Log_out(self):
        print('Bye~' + self.userInfo['User']['NickName'])
