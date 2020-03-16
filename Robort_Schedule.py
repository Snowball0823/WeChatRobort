import datetime
import time


def SearchMyClass(msg, UserOwn):
    reply_Num = UserOwn.SearchClass.index(msg.text)
    # print('reply_Num='+str(reply_Num))
    TimeNow = time.localtime(time.time())
    hourNow = TimeNow[3]
    hourDiff = 24
    weekToday = UserOwn.weekDay[str(TimeNow[6])]
    weekTomorr = UserOwn.weekDay[str(TimeNow[6] + 1)]
    weekNow = datetime.date(TimeNow[0], TimeNow[1],
                            TimeNow[2]) - datetime.date(2018, 2, 26)
    weekNow = int(str(weekNow).split('d')[0])
    weekNow = int(weekNow / 7) + 1
    weekNext = datetime.date(TimeNow[0], TimeNow[1],
                             TimeNow[2] + 1) - datetime.date(2018, 2, 26)
    weekNext = int(str(weekNext).split('d')[0])
    weekNext = int(weekNext / 7) + 1
    weekDu = weekNow % 2
    weekDuNext = weekNext % 2
    reply_One = reply_Two = reply_Three = reply_Four = reply_Five = reply_Six = reply_Seven = reply_Eight = reply_Nine = reply_Ten = reply_Eleven = reply_Twelve = reply_Tmp_1 = reply_Tmp_2 = ''
    reply_Three = UserOwn.ClassStr
    reply_Six = '这周是第' + str(weekNow) + '周噢小主人'
    # print('reply_Three='+reply_Three)
    if reply_Num == 0 or reply_Num == 1 or reply_Num == 4 or reply_Num == 7 or reply_Num == 8 or reply_Num == 9:
        # print('Today='+weekToday)
        # print('')
        for classInfoTmp in UserOwn.ClassTable[weekToday]:
            try:
                # print(classInfoTmp)
                # print(classInfoTmp[6])
                # +' '+str(int(classInfoTmp[8])%2)+' '+weekDu+' '+classInfoTmp[6]+' '+classInfoTmp[7])
                if int(classInfoTmp[0]) >= int(hourNow) and (int(
                        classInfoTmp[2]) - int(hourNow)) < hourDiff and (
                            classInfoTmp[8] == '0'
                            or int(classInfoTmp[8]) % 2 == weekDu) and (
                                weekNow >= int(classInfoTmp[6])
                                and weekNow <= int(classInfoTmp[7])):
                    hourDiff = int(classInfoTmp[2]) - hourNow
                    reply_One = u'下节课: \n' + classInfoTmp[
                        0] + ':' + classInfoTmp[1] + '~' + classInfoTmp[
                            2] + ':' + classInfoTmp[
                                3] + '\n' + u'教室: ' + classInfoTmp[
                                    4] + u'\n' + u'课程: ' + classInfoTmp[
                                        5] + '\n'
                    delayTime = int(classInfoTmp[0]) * 60 + int(
                        classInfoTmp[1]) - int(TimeNow[3] * 60) - int(
                            TimeNow[3])
                    #print(str(int(TimeNow[2]*60))+' '+str(TimeNow[2]))
                    # print(delayTime)
                    delayHour = int(delayTime / 60)
                    delayMin = delayTime % 60
                    if delayHour == 0 and delayMin >= 20:
                        delayTime = str(delayMin) + '分钟'
                    elif delayHour == 0 and delayMin < 20:
                        delayTime = str(delayMin) + '分钟,小主人要加快了噢，要迟到了～'
                    else:
                        delayTime = str(delayHour) + '小时' + str(
                            delayMin) + '分钟'
                    # print(delayTime)
                    reply_Five = u'主人,下节课在' + classInfoTmp[
                        4] + u'上课噢~\n' + u'下节课上课时间是: \n' + classInfoTmp[
                            0] + ':' + classInfoTmp[
                                1] + '\n' + '距离上课还有:' + delayTime
                else:
                    pass
                #print(classInfoTmp[8]+' '+str(int(classInfoTmp[8])%2)+' '+weekDu+' '+classInfoTmp[6]+' '+classInfoTmp[7])
                if (classInfoTmp[8] == '0'
                        or int(classInfoTmp[8]) % 2 == weekDu) and (
                            weekNow >= int(classInfoTmp[6])
                            and weekNow <= int(classInfoTmp[7])):
                    reply_Two = reply_Two + classInfoTmp[
                        0] + ':' + classInfoTmp[1] + '~' + classInfoTmp[
                            2] + ':' + classInfoTmp[
                                3] + '\n' + u'教室: ' + classInfoTmp[
                                    4] + '\n' + u'课程: ' + classInfoTmp[
                                        5] + '\n'
                    reply_Eight = u'小主人今天有课噢～这是今天的课表:\n' + reply_Two
                    # print('reply_Eight='+reply_Eight)
                else:
                    pass
                if (classInfoTmp[8] == '0'
                        or int(classInfoTmp[8]) % 2 == weekDu) and (
                            int(weekNow) >= int(classInfoTmp[6])
                            and int(weekNow) <= int(classInfoTmp[7])
                ) and int(classInfoTmp[0]) < 12:
                    reply_Tmp_1 = reply_Tmp_1 + classInfoTmp[
                        0] + ':' + classInfoTmp[1] + '~' + classInfoTmp[
                            2] + ':' + classInfoTmp[
                                3] + '\n' + u'教室: ' + classInfoTmp[
                                    4] + '\n' + u'课程: ' + classInfoTmp[
                                        5] + '\n'
                    reply_Ten = u'主人，上午的课表是:\n' + reply_Tmp_1
                elif (classInfoTmp[8] == '0'
                        or int(classInfoTmp[8]) % 2 == weekDu) and (
                            int(weekNow) >= int(classInfoTmp[6])
                            and int(weekNow) <= int(classInfoTmp[7])) and (
                                int(classInfoTmp[0]) > 12
                                and int(classInfoTmp[2]) < 23):
                    reply_Tmp_2 = reply_Tmp_2 + classInfoTmp[
                        0] + ':' + classInfoTmp[1] + '~' + classInfoTmp[
                            2] + ':' + classInfoTmp[
                                3] + '\n' + u'教室: ' + classInfoTmp[
                                    4] + '\n' + u'课程: ' + classInfoTmp[
                                        5] + '\n'
                    reply_Nine = u'主人，下午的课表是:\n' + reply_Tmp_2
                else:
                    pass
            except Exception as error:
                print('You have today wrong!\n' + str(error))
                if weekToday == u'周六' or weekToday == u'周日':
                    reply_One = reply_Two = reply_Five = reply_Eight = reply_Nine = reply_Ten = u'主人今天是周末哦～没有课😊'
                else:
                    pass
    elif reply_Num == 3 or reply_Num == 6 or reply_Num == 10 or reply_Num == 11:
        for classInfoTmp in UserOwn.ClassTable[weekTomorr]:
            try:
                if (classInfoTmp[8] == '0'
                        or int(classInfoTmp[8]) % 2 == weekDuNext) and (
                            weekNext >= int(classInfoTmp[6])
                            and weekNext <= int(classInfoTmp[7])):
                    reply_Four = reply_Four + classInfoTmp[
                        0] + ':' + classInfoTmp[1] + '~' + classInfoTmp[
                            2] + ':' + classInfoTmp[
                                3] + '\n' + u'教室: ' + classInfoTmp[
                                    4] + '\n' + u'课程: ' + classInfoTmp[
                                        5] + '\n'
                    reply_Seven = u'小主人,明天有课噢～这是明天的课表:\n' + reply_Four
                else:
                    pass
                if (classInfoTmp[8] == '0'
                        or int(classInfoTmp[8]) % 2 == weekDuNext) and (
                            weekNow >= int(classInfoTmp[6])
                            and int(weekNow) <= int(classInfoTmp[7])
                ) and int(classInfoTmp[0]) < 12:
                    reply_Tmp_1 = reply_Tmp_1 + classInfoTmp[
                        0] + ':' + classInfoTmp[1] + '~' + classInfoTmp[
                            2] + ':' + classInfoTmp[
                                3] + '\n' + u'教室: ' + classInfoTmp[
                                    4] + '\n' + u'课程: ' + classInfoTmp[
                                        5] + '\n'
                    reply_Eleven = u'主人，明天上午的课表是:\n' + reply_Tmp_1
                elif (classInfoTmp[8] == '0'
                        or int(classInfoTmp[8]) % 2 == weekDu) and (
                            int(weekNow) >= int(classInfoTmp[6])
                            and int(weekNow) <= int(classInfoTmp[7])) and (
                                int(classInfoTmp[0]) > 12
                                and int(classInfoTmp[2]) < 23):
                    reply_Tmp_2 = reply_Tmp_2 + classInfoTmp[
                        0] + ':' + classInfoTmp[1] + '~' + classInfoTmp[
                            2] + ':' + classInfoTmp[
                                3] + '\n' + u'教室: ' + classInfoTmp[
                                    4] + '\n' + u'课程: ' + classInfoTmp[
                                        5] + '\n'
                    reply_Twelve = u'主人，明天下午的课表是:\n' + reply_Tmp_2
                else:
                    pass
            except Exception as error:
                print('You have tomorrow wrong!\n' + str(error))
                if weekTomorr == u'周六' or weekTomorr == u'周日':
                    reply_Four = reply_Seven = reply_Eleven = reply_Twelve = u'主人明天是周末哦～没有课😊'
                else:
                    pass
    else:
        pass
    reply_All = [
        reply_One, reply_Two, reply_Three, reply_Four, reply_Five,
        reply_Six, reply_Seven, reply_Eight, reply_Nine, reply_Ten,
        reply_Eleven, reply_Twelve
    ]
    for i in reply_All:
        if i == '':
            numTmp = reply_All.index(i)
            reply_All[numTmp] = UserOwn.ClassRelax[numTmp]
        else:
            pass
    # print('Result='+str(reply_All[reply_Num]))
    return reply_All[reply_Num]
