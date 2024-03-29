#/bin/env python
# coding: utf-8

__author__ = 'Martin Horak, Pavel Studenik'
__version__ = 0.2

try: 
    import gtk
    import pygtk
    import os
    import sys
    import time
    import pynotify
    import imaplib
    import ConfigParser
    import sqlite3
    import email
    import re
    import getopt
    import getpass
    pygtk.require('2.0')
except:
    print("Error: %s" % "need python-notify, imaplib, python-gtk2 and gtk")
    sys.exit(1)

str_file_config =  \
"""# ban.conf

[Info]
hostname=%s
username=%s
password=%s
mark=%s
"""
    
class Config():
    
    def __init__(self):
        # change to /etc after write install script
        fileconfig = 'settings.conf'
        self.config = ConfigParser.ConfigParser()
        if os.path.exists(fileconfig):
            self.config.read(os.path.realpath(fileconfig))
        else:
            f=open(fileconfig,'w')
            print("DEBUG: File %s doesn't exist" % fileconfig)
            print("DEBUG: File %s create. Yum must set up value for email." % fileconfig)

            hostname = raw_input("Enter your hostname: ")
            username = raw_input("Enter your username: ")
            password = getpass.getpass("Enter your password: ")
            mark = raw_input("Select mark (inbox): ")
            str_file_config_output = (str_file_config) % (hostname, username, password, mark)
            f.write(str_file_config_output)
            f.close()
            # read config file
            self.config.read(os.path.realpath(fileconfig))
        
    def get_hostname(self):
        return self.config.get('Info','hostname')

    def get_username(self):
        return self.config.get('Info','username')
    
    def get_password(self):
        return self.config.get('Info','password')
    
    def get_mark(self):
        return self.config.get('Info','mark')
    
class DatabaseResources():
    """
    Class for handling with database.
    For more info http://docs.python.org/library/sqlite3.html
    
    """
    
    def __init__(self):
        self.conn = sqlite3.connect('KB.db')
        self.c = conn.cursor()
    
    """
    def somefce(self):
        c.execute("SQL COMMAND")
    """

class BankAccountEmail():
    """
    Class for parsing data from emails.
    
    """

    def __init__(self):
        conf = Config()
        self.conn = imaplib.IMAP4_SSL(conf.get_hostname())
        self.conn.login(conf.get_username(), conf.get_password()) 
        self.mark = conf.get_mark()
        
    def getList(self):
        print self.conn
        typ, data = self.conn.list()
        if typ == "OK":
            print("DEBUG: Data load ok") 
            for it in data:
                print it 
            #TODO check if mark exists
        else: 
            print("ERROR: Data didn't load") 

    def getParseEmail(self, raw_data):
        def parse(raw_data):
            msg = raw_data.split("\n")[0]
            m = re.search(" ([0-9, ]*) CZK", msg)
            value = m.group(1).replace(",",".").replace(" ","")
            return {"message": msg, "value": float(value) }

        email_message = email.message_from_string(raw_data[0][1])
        data = {"id": email_message["subject"] }
        maintype = email_message.get_content_maintype()
        if maintype == 'multipart':
            for part in email_message.get_payload():
                if part.get_content_maintype() == 'text':
                    data.update( parse(part.get_payload(decode=True)))
        elif maintype == 'text':
            data.update( parse(email_message_instance.get_payload()) )
        return data

    def getActual(self):
        #self.getList()

        self.conn.select(self.mark)
        #result, data = self.conn.uid('search', None, "ALL")
        result, data = self.conn.uid('search', None, "UNSEEN")
        for email_uid in data[0].split()[-1:]: # only last second emails
            result, raw_email = self.conn.uid('fetch', int(email_uid), '(RFC822)')
            return self.getParseEmail(raw_email)

    def getAll(self, debug=False):
        self.getList()
        msg_list = []
        self.conn.select(self.mark)
        result, data = self.conn.uid('search', None, '(HEADER from "info@kb.cz")')
        for email_uid in reversed(data[0].split()):
            result, raw_email = self.conn.uid('fetch', int(email_uid), '(RFC822)')
            try:
                msg_list += self.getParseEmail(raw_email)
                if debug:
                    print self.getParseEmail(raw_email)
            except:
                print "ERROR: %s" % raw_email

        return msg_list


class NotifierUnity():
    """
    Class for handling with notifications.
    
    """
    
    def __init__(self):
        pynotify.init("Bank account notification")
        pic_file = 'kb_logo.svg'
        self.pic = 'data/' + pic_file
        
    def show(self, ntf_title, ntf_str):

        if not os.path.exists(self.pic):
            print "DEBUG: image %s doesn't exists" % self.pic

        n = pynotify.Notification(ntf_title, ntf_str, self.pic)
        # n.set_urgency(pynotify.URGENCY_CRITICAL)
        # n.set_category("device")
        n.set_timeout(10000)
        n.show()

if __name__ == "__main__":

    ptlist, args = getopt.getopt(sys.argv[1:], 'd', ["only-parse", "run"])

    __run__ = True
    b_account = BankAccountEmail()
    u_notify = NotifierUnity()

    # print all data for archive action with bank's account
    if ptlist != [] and "--only-parse" in ptlist[0]:
        __run__=False
        b_account.getAll(debug=True)

    # show data in gnome notify
    while(__run__):
        d = b_account.getActual()
        if d:
            msg = d["message"].decode(encoding="cp1250")
            #u_notify.show("My bank account", "%.2f CZK" % (d["value"]))
            u_notify.show("My bank account", "%s" % (msg))

        if ptlist != [] and "--run" in ptlist[0]:
            time.sleep(60)
        else:
            __run__ = False

