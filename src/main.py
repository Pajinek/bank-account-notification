#/bin/env python
# coding: utf-8

try: 
    import gtk, pygtk, os
    import sys
    import pynotify
    pygtk.require('2.0')
except:
    print("Error: %s" % "need python-notify, python-gtk2 and gtk")
    sys.exit(1)


class BankAccountEmail():
    """
    Class for parsing data from emails.
    
    """

    def getActual(self):
        return -10**5


class NotifierUnity():
    """
    Class for handling with notifications.
    
    """
    
    def __init__(self):
        pynotify.init("Bank account notification")
        
    def show(self, ntf_title, ntf_str):
        
        n = pynotify.Notification(ntf_title, ntf_str)
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

