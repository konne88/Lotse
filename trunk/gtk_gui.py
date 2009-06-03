#!/usr/bin/env python
#coding=utf-8

#import osso
#import hildon
import gtk
import gobject
import coordinates

import gps, os, time, sys
from math import *  
 

class Lotse:
    def __init__(self):
            #   osso_c = osso.Context("osso_test_app", "0.0.1", False)
        #  self.program  = hildon.Program()
        #  self.window = hildon.Window()
        self.window = gtk.Window()
        self.LatLabel = gtk.Label("")
        self.LonLabel = gtk.Label("")
        self.AltLabel = gtk.Label("")
        self.VelLabel = gtk.Label("")
        self.HeadLabel = gtk.Label("")
        self.HBox = gtk.HBox()
        self.VBoxLeft= gtk.VBox()
        self.VBoxRight = gtk.VBox()
        
        self.ListTargetCombo = gtk.combo_box_new_text()
        self.CoordEntry = gtk.Entry()
        self.TargetAddButton = gtk.Button("Add Target Coordinates")
        
        
        self.HBox.add(self.VBoxLeft)
        self.HBox.add(self.VBoxRight)
        
        self.VBoxLeft.add(self.LatLabel)
        self.VBoxLeft.add(self.LonLabel)
        self.VBoxLeft.add(self.AltLabel)
        self.VBoxLeft.add(self.VelLabel)
        self.VBoxLeft.add(self.HeadLabel)
        
        self.VBoxRight.add(self.ListTargetCombo)
        self.VBoxRight.add(self.CoordEntry)
        self.VBoxRight.add(self.TargetAddButton)
        
        self.window.add(self.HBox)
        self.session = gps.gps()
        
        gobject.timeout_add(100, self.update_widget)
            
        self.window.connect('destroy', self.window_destroy)
        self.TargetAddButton.connect('clicked',self.button_clicked)
        self.window.show_all()

    def button_clicked(self, widget, data=None):
        self.ListTargetCombo.append_text(self.CoordEntry.get_text())
        self.ListTargetCombo.set_active()
        
    
    def window_destroy(self,widget, data=None):
        gtk.main_quit()

    def main(self):
        gtk.main()


    def update_widget(self):
        self.session.query('admosy')

       
        self.LatLabel.set_text('Lat: %.5f °'%self.session.fix.latitude)
        self.LonLabel.set_text('Lon: %.5f °'%self.session.fix.longitude)
        self.AltLabel.set_text('Altitude: %.0f m'%self.session.fix.altitude)
        self.VelLabel.set_text('Speed: %.5f m/s'%self.session.fix.speed)
        self.HeadLabel.set_text('Heading: %.1f °'%self.session.fix.track) 
    
        return 1



# If the program is run directly or passed as an argument to the python
# interpreter then create a HelloWorld instance and show it
if __name__ == "__main__":
    Lotse = Lotse()
    Lotse.main()
