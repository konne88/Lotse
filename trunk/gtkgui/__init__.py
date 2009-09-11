#coding=utf-8

#import osso
#import hildon
import  os, time, sys

import gtk

#from source_tab import SourceTab
from goto_tab import GotoTab
from waypoint_tab import WaypointTab
from log_tab import LogTab
from status_box import StatusBox

#class LotseWindow(hildon.Window):
class LotseWindow(gtk.Window):
    def __init__(self,session):
        super(LotseWindow,self).__init__()
        
        self._session = session
        self._mainbox = gtk.VBox()
        self.add(self._mainbox)
    
        self._notebook = gtk.Notebook()        
        self._mainbox.pack_start(self._notebook)
       
       
        self._gotoTab = GotoTab(session)
        self._notebook.append_page(self._gotoTab, gtk.Label('Goto'))
        

        
        self._waypointTab = WaypointTab(session)
        self._notebook.append_page(self._waypointTab, gtk.Label('Waypoints'))
        
        self._logTab = LogTab(session)
        self._notebook.append_page(self._logTab, gtk.Label('Log'))

        self._status_box = StatusBox(self._session)
        self._mainbox.pack_start(self._status_box, False, False)

        self.connect('destroy', self.window_destroy)
        self.set_geometry_hints(None,640,480)
        
        self.show_all()
        gtk.main()
    
    def window_destroy(self,widget, data=None):
        self._session.save_persistent()    
        gtk.main_quit()

