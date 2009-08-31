#coding=utf-8

import gtk
import gobject
import os
import time

from session.waypoint import Waypoint
from session.coordinates import Coordinates
from session import Session
from radar import Radar
from session.logger import Logger
from session.gpxlogger import GPXLogger

class LogTab(gtk.VBox):
    def __init__(self,session):
        super(LogTab,self).__init__()
        self._session=session

        self._loginfo = gtk.Label()        

        bBox= gtk.VButtonBox()
        bBox.set_layout(gtk.BUTTONBOX_START)
        self._start = gtk.Button('Start Logging')
        self._stop = gtk.Button('Pause logging')
        self._end = gtk.Button('End Logging')      

        bBox.pack_start(self._start, False,False)
        bBox.pack_start(self._stop, False,False)
        bBox.pack_start(self._end, False,False)

        self.pack_start(self._loginfo)
        self.pack_start(bBox)

        self._start.connect('clicked',self.on_start)
        self._stop.connect('clicked',self.on_stop)
        self._end.connect('clicked',self.on_end)
        self._logger = None #So that we can test for it

        
    def create_logger(self):
        dialog = gtk.FileChooserDialog("Open..",
                               None,
                               gtk.FILE_CHOOSER_ACTION_SAVE,
                               (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)

        #filter = gtk.FileFilter()
        #filter.set_name("All files")
        #filter.add_pattern("*")
        #dialog.add_filter(filter)
        filter = gtk.FileFilter()
        filter.set_name("Waypoints")
        filter.add_pattern("*.gpx")
        filter.add_pattern("*.GPX")
        #filter.add_pattern("*.kml")
        #filter.add_pattern("*.KML")      
        dialog.add_filter(filter)


        response = dialog.run()
        if response == gtk.RESPONSE_OK:

            self._logger = GPXLogger(self._session, dialog.get_filename())
            self._logger.status_changed += self.on_status_changed
            self.on_status_changed(self._logger)
            dialog.destroy()
            return True
        else:
            dialog.destroy()
            return False
           
            

    def on_start(self, widget, data=None):
        if self._logger != None:
            self._logger.stop()
            self._logger = None    
            
        if self.create_logger():
            self._logger.start()

    def on_stop(self, widget, data=None):
        if self._logger != None:
            self._logger.stop()

    def on_end(self, widget, data=None):
        if self._logger != None:
            self._logger.stop()
            self._logger = None


    def on_status_changed(self, sender):
        s=sender.name+'\n'+('Not Running','Running')[int(sender.running)]
        self._loginfo.set_text(s)

