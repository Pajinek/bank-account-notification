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


def show_notify(str_ntf):
    pynotify.init("Bank account notification")
    n = pynotify.Notification("Aktuální zůstatek", "%d Kč" % str_ntf)
    n.set_timeout(10000)
    n.show()

if __name__ == "__main__":
    show_notify(1000)
