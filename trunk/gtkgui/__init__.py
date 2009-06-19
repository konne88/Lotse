#coding=utf-8

#import osso
import hildon
import  os, time, sys

import gtk

from source_tab import SourceTab
from goto_tab import GotoTab
from waypoint_tab import WaypointTab

class LotseWindow(hildon.Window):
#class LotseWindow(gtk.Window):
    def __init__(self,session):
        super(LotseWindow,self).__init__()
        
        self._session = session
        self._notebook = gtk.Notebook()
        self.add(self._notebook)
        
        self._gotoTab = GotoTab(session)
        self._notebook.append_page(self._gotoTab, gtk.Label('Goto'))
        
        self._sourceTab = SourceTab(session)
        self._notebook.append_page(self._sourceTab, gtk.Label('Sources'))
        
        self._waypointTab = WaypointTab(session)
        self._notebook.append_page(self._waypointTab, gtk.Label('Waypoints'))

        self.connect('destroy', self.window_destroy)
        self.set_geometry_hints(None,640,480)
        self.show_all()
        
        gtk.main()
    
    def window_destroy(self,widget, data=None):
        self._session.save_persistent()    
        gtk.main_quit()

