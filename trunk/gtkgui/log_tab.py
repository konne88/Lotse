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
        
        self._logger = GPXLogger(self._session, 'log.xml')
        
    
    def on_start(self, widget, data=None):
        self._logger.start()
    
    def on_stop(self, widget, data=None):
        self._logger.stop()
    
    def on_end(self, widget, data=None):
        self._logger.end()
        
