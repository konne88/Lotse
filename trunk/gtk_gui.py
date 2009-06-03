#!/usr/bin/env python
#coding=utf-8

#import osso
#import hildon
import gtk
import gobject

import gps, os, time, sys
from math import *  
 
 def update_widget(session, infolabel):
    session.query('admosy')

    infostring=''
    infostring+='Status: '+str(session.status)+'\n'
    infostring+='Latitude: %.5f'%session.fix.latitude+'\n'
    infostring+='Longitude: %.5f'%session.fix.longitude+'\n'
    infostring+='Speed: %.5f'%session.fix.speed+' m/s\n'
    infostring+='Track: %.5f'%session.fix.track+'\n'
    infostring+='Altitude: %.0f'%session.fix.altitude+' m\n'

    infostring+='Time (UTC): '+session.utc+'\n'

    infolabel.set_text(infostring)
    return 1

def window_destroy(widget, data=None):
    gtk.main_quit()

def main():
    #   osso_c = osso.Context("osso_test_app", "0.0.1", False)
    #  program  = hildon.Program()
    #  window = hildon.Window()
    window = gtk.Window()
    label = gtk.Label("")
    label.set_text('test')
    window.add(label)
    session = gps.gps()
    gobject.timeout_add(100, update_widget, session, label)
    window.show_all()
    window.connect('destroy', window_destroy)
    gtk.main()

if __name__ == "__main__":
    main()
