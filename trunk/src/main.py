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


def show_notify(ntf_title, ntf_str):
    pynotify.init("Bank account notification")
    n = pynotify.Notification(ntf_title, ntf_str)
    # n.set_urgency(pynotify.URGENCY_CRITICAL)
    # n.set_category("device")
    n.set_timeout(10000)
    n.show()

if __name__ == "__main__":
    show_notify("Aktuální zůstatek", "1000 Kč")
