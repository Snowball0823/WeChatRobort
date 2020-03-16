import select
import sys
import termios
import threading

import itchat

import _thread


class KeyBoard(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def reSet(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        new_settings = old_settings
        #new_settings[3] = new_settings[3] & ~termios.ISIG
        new_settings[3] = new_settings[3] & ~termios.ICANON
        new_settings[3] = new_settings[3] & ~termios.ECHONL
        termios.tcsetattr(fd, termios.TCSAFLUSH, new_settings)

    def kbhit(self):
        fd = sys.stdin.fileno()
        r = select.select([sys.stdin], [], [], 2)
        rcode = True
        if len(r[0]) > 0:
            #rcode  = sys.stdin.read(1)
            rcode = False
        return rcode

    def run(self):
        key_Tmp = True
        while key_Tmp:
            key_Tmp = self.kbhit()
        if ~key_Tmp:
            ReplyMsg = 'Snowball Robort Closing now!'
            itchat.send(ReplyMsg, toUserName='filehelper')
            itchat.logout()
