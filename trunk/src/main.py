#/bin/env python
# coding: utf-8

__author__ = 'Martin Horak, Pavel Studenik'
__version__ = 0.1

try: 
    import gtk
    import pygtk
    import os
    import sys
    import pynotify
    import imaplib
    import ConfigParser
    pygtk.require('2.0')
except:
    print("Error: %s" % "need python-notify, imaplib, python-gtk2 and gtk")
    sys.exit(1)

    
class Config():
    
    def __init__(self):
        self.config = ConfigParser.ConfigParser()
        self.config.read(os.path.realpath('src/ban.conf'))
         # change to /etc after write install script
        
    def get_hostname(self):
        return self.config.get('Info','hostname')

    def get_username(self):
        return self.config.get('Info','username')
    
    def get_password(self):
        return self.config.get('Info','password')   


class BankAccountEmail():
    """
    Class for parsing data from emails.
    
    """
    hostname = "imap.gmail.com"
    username = "horak@styrax.info" 
    password = "7cx34ymbwn"

    def __init__(self):
        conf = Config()
        self.conn = imaplib.IMAP4_SSL(conf.get_hostname())
        self.conn.login(conf.get_username(), conf.get_password()) 
        
    def getList(self):
        print self.conn
        typ, data = self.conn.list()

        print typ
        for it in data:
            print it 

        self.conn.select("inbox")
        result, data = self.conn.uid('search', None, "ALL")
        for email_uid in data[0].split()[-2:]: # only last second emails
            print email_uid
            result, data = self.conn.uid('fetch', int(email_uid), '(RFC822)')
            print result, data


    def getActual(self):
        self.getList()
        return -10**5


class NotifierUnity():
    """
    Class for handling with notifications.
    
    """
    
    def __init__(self):
        pynotify.init("Bank account notification")
        pic_file = 'kb_logo.svg'
        self.pic = os.path.abspath('..') + '/data/' + pic_file
        
    def show(self, ntf_title, ntf_str):
        
        print self.pic
        n = pynotify.Notification(ntf_title, ntf_str, self.pic)
        # n.set_urgency(pynotify.URGENCY_CRITICAL)
        # n.set_category("device")
        n.set_timeout(10000)
        n.show()

if __name__ == "__main__":

    __run__ = True
    b_account = BankAccountEmail()
    u_notify = NotifierUnity()

    while(__run__):
        d = b_account.getActual()
        u_notify.show("My bank account", "%d CZK" % d)
        # temporary value for testing
        __run__ = False

