#!/usr/bin/env python
#coding=utf-8

#import osso
#import hildon
import gtk
import gobject

import gps, os, time, sys
from math import *  
 

class Lotse:
    def __init__(self):
            #   osso_c = osso.Context("osso_test_app", "0.0.1", False)
        #  self.program  = hildon.Program()
        #  self.window = hildon.Window()
        self.window = gtk.Window()
        self.infolabel = gtk.Label("")
        self.window.add(self.infolabel)
        self.session = gps.gps()
        
        gobject.timeout_add(1000,\
            self.update_widget, \
            self.session, self.infolabel)
            
        self.window.connect('destroy', self.window_destroy)
        self.window.show_all()

    def window_destroy(self,widget, data=None):
        gtk.main_quit()

    def main(self):
        gtk.main()


    def update_widget(self, session, infolabel):
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



# If the program is run directly or passed as an argument to the python
# interpreter then create a HelloWorld instance and show it
if __name__ == "__main__":
    Lotse = Lotse()
    Lotse.main()
